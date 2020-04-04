from __future__ import print_function, division
import torch
from tqdm.autonotebook import tqdm
import copy
import os
from torch.optim.lr_scheduler import _LRScheduler
import matplotlib.pyplot as plt

class LRFinder(object):
    """
    Input:
        model : DNN model
        optimizer : optimizer where the defined learning is assumed to be the lower boundary of the range test
        criterion : Loss function
        device : represents the device on which the computation will take place.
        memory_cache : If true, 'state_dict' of the model and optimizer will be cached in memory. Otherwise saved to files under 'cache_dir'
    
    """
    
    def __init__(self, model, optimizer, criterion, device, memory_cache=True, cache_dir=None):
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.best_loss = None
        self.memory_cache = memory_cache
        self.cache_dir = cache_dir
        
        self.history = {"lr": [], "Loss": [], "Acc": []}
        
        if device:
            self.device = device
        else:
            self.device = self.model_device
            
        # Save the original state of the model and optimizer
        self.model_device = next(self.model.parameters()).device
        self.state_cacher = StateCacher(memory_cache, cache_dir=cache_dir)
        self.state_cacher.store("model", self.model.state_dict())
        self.state_cacher.store("optimizer", self.optimizer.state_dict())
        
    def reset(self):
        """Restores the model and optimizer to their initial states."""

        self.model.load_state_dict(self.state_cacher.retrieve("model"))
        self.optimizer.load_state_dict(self.state_cacher.retrieve("optimizer"))
        self.model.to(self.model_device)
        
        
    
    def range_test(self, trainloader, testloader=None, start_lr=None, end_lr=2, num_iter=100, step_mode="linear", smooth_f=0.05, diverge_th=5, accumulation_steps=1):
        """
        Input:
            trainloader : Training set data loader
            testloader : Test set data loader
            start_lr : starting Learning rate for the range test. (Default=None, uses the learning rate from the optimizer)
            end_lr : the last learning rate upto which range test is done. (Default=2)
            num_iter : number of iterations over which test occurs. (Default=100)
            step_mode : Learning rate policy. Either linear or exponential. (Default="linear")
            smooth_f : Loss smoothing factor. [0,1)  (Default=0.05)
            diverge_th : test is stopped when loss surpasses the diverge threshold, calculated to be- diverge_th * best_loss (Default=5)
            accumulation_steps: steps for gradient accumulation.
        Output:
            
        """
         
        #Reset test results
        self.history = {"lr": [], "Loss": [], "Acc": []}
        self.best_loss = None
        
        #Move model to device
        self.model.to(self.device)
        
        if start_lr:
            self._set_learning_rate(start_lr)
        
        #Initialize Learning rate policy.Using either "linear" or "exp". Error otherwise.
        if step_mode.lower() == "linear":
            lr_schedule = LinearLR(self.optimizer, end_lr, num_iter)
        elif step_mode.lower() == 'exp':
            lr_schedule = ExponentialLR(self.optimizer, end_lr, num_iter)
        else:
            raise ValueError("Learning rate policy should be either linear or exp. Received {} as the LR policy".format(step_mode))
            
        
        if smooth_f < 0 or smooth_f >= 1:
            raise ValueError("smooth_f is outside the range [0, 1)")
        
        
        #Training model begins.
        # Iterator to get data by batches.
        iter_wrapper = DataLoaderIterWrapper(trainloader)
        #Train and test on the batches
        for iteration in tqdm(range(num_iter)):
            accuracy, loss = self._train_batch(iter_wrapper, accumulation_steps)
            
            if testloader:
                accuracy, loss = self._validate(testloader)
        
            #Update Learning rate
            lr_schedule.step()
            self.history["lr"].append(lr_schedule.get_lr()[0])
        
            # Track the best loss
            if iteration == 0:
                self.best_loss = loss
            else:
                if smooth_f > 0:
                    loss = smooth_f * loss + (1 - smooth_f) * self.history["Loss"][-1]
                
                if loss < self.best_loss:
                    self.best_loss = loss

            # Check if the loss has diverged; if it has, stop the test
            self.history["Loss"].append(loss)
            self.history["Acc"].append(accuracy)
            # print("Run iteration:",iteration,"  Test LR",self.history["lr"][-1], "  Test loss:",loss,"  Test Accuracy:",accuracy)
        
            if loss > diverge_th * self.best_loss:
                print("Stopping early, the loss has diverged")
                break

        print("Learning rate search finished. See the graph with {finder_name}.plot()")
            
            
            
            
    
    
    # Set learning rate.
    def _set_learning_rate(self, new_lrs):
        if not isinstance(new_lrs, list): # check if its a list
            new_lrs = new_lrs * len(self.optimizer.param_groups) #TODO- check this
        if len(new_lrs) != len(self.optimizer.param_groups):
            raise ValueError("Length of new LRs are not equal to number of parameter groups in the optimizer")
        
        #TODO- check this
        for param_group, new_lr in zip(self.optimizer.param_groups, new_lrs):
            param_group["lr"] = new_lr
            
    

    #Training the model
    def _train_batch(self, iter_wrapper, accumulation_steps):
        total_loss = None
        train_accuracy = 0
        correct = 0
        total = 0
        
        self.model.train()
        
        #Train
        self.optimizer.zero_grad()
        for i in range(accumulation_steps):
            inputs, labels = iter_wrapper.get_batch()
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)
            #Forward pass
            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)
            #Average loss
            loss /= accumulation_steps
            #backward pass
            loss.backward()
            
            pred = outputs.argmax(dim=1, keepdim=True)
            correct += pred.eq(labels.view_as(pred)).sum().item()
            total += len(inputs)
            
            if total_loss is None:
                total_loss = loss
                train_accuracy = (100 * correct)/total
            else:
                total_loss += loss
                train_accuracy += (100 * correct)/total
            
            # print("Train batch size",inputs.size(0))
        self.optimizer.step()
            
        return train_accuracy, total_loss.item()
            
    
    #Testing the model
    def _validate(self, dataloader):
        #set in eval mode to disable gradient accumulation
        correct = 0
        total = 0
        epoch_test_loss = 0.0
        epoch_test_accuracy = 0
        self.model.eval()
        with torch.no_grad():
            for inputs, labels in dataloader:
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                outputs = self.model(inputs)
                
                if isinstance(inputs, tuple) or isinstance(inputs, list):
                    batch_size = inputs[0].size(0)
                else:
                    batch_size = inputs.size(0)
                    
                epoch_test_loss += self.criterion(outputs, labels).item()
                _, predicted = torch.max(outputs.data, 1)
                total += batch_size
                correct += (predicted == labels).sum().item()
    
        epoch_test_accuracy = (100 * correct / total)
        epoch_test_loss /= len(dataloader)
        return epoch_test_accuracy, epoch_test_loss
    
    def plot(self, skip_start=10, skip_end=5, log_lr=True, show_lr=None, ax=None):
        """
        Plot the learning rate range test
        
        skip_start : number of batches to trim from the start. (Default=10)
        skip_end : number of batches to trim from the end. (Default=5)
        log_lr : To plot the learning rate graph in logarithmic scale, linear otherwise. (Default=True for log scale)
        show_lr : Add a vertical line to visualize the learning rate. (Default=None)
        ax : Matplotlib figure
        """
        
        lrs = self.history["lr"]
        loss = self.history["Loss"]
        acc = self.history["Acc"]
        
        if skip_end == 0:
            lrs = lrs[skip_start:]
            loss = loss[skip_start:]
            acc = acc[skip_start:]
        else:
            lrs = lrs[skip_start:-skip_end]
            loss = loss[skip_start:-skip_end]
            acc = acc[skip_start:-skip_end]
        
        #Create figure and axes
        fig = None
        if ax is None:
            fig, ax = plt.subplots(1,2,figsize=(15,7.5))
        
        #Plot validation loss and accuracy against Learning rate.
        ax[0].plot(lrs, loss)
        ax[1].plot(lrs, acc)
        if log_lr:
            ax[0].set_xscale("log")
            ax[1].set_xscale("log")
        ax[0].set_title("Loss vs Learning rate")
        ax[0].set_xlabel("Learning rate")
        ax[0].set_ylabel("Loss")
        
        ax[1].set_title("Accuracy vs Learning rate")
        ax[1].set_xlabel("Learning rate")
        ax[1].set_ylabel("Accuracy")
        if show_lr:
            ax[0].axvline(x=show_lr, color="red")
            ax[1].axvline(x=show_lr, color="red")

        if fig is not None:
            plt.show()
        
        return ax
        

# Setup linear schedule for Learning rate
class LinearLR(_LRScheduler):
    """
    To schedule linear learning rate between 2 boundaries over a given number of iterations.
    
    Input:
    optimizer : Optimizer for the model
    end_lr : Final learning rate
    num_iter : Number of iterations over which test occurs.
    last_epoch : Index of the final epoch
    
    """
    def __init__(self, optimizer, end_lr, num_iter, last_epoch=-1):
        self.end_lr = end_lr
        self.num_iter = num_iter
        super(LinearLR, self).__init__(optimizer, last_epoch)
        
    def get_lr(self):
        curr_iter = self.last_epoch + 1
        r = curr_iter/self.num_iter
        return [base_lr + r * (self.end_lr - base_lr) for base_lr in self.base_lrs]
        

# Setup exponential schedule for learning rate
class ExponentialLR(_LRScheduler):
    """Exponentially increases the learning rate between two boundaries over a number of iterations.
    Input:
    optimizer : Optimizer for the model
    end_lr : Final learning rate
    num_iter : Number of iterations over which test occurs.
    last_epoch : Index of the final epoch
    
    """

    def __init__(self, optimizer, end_lr, num_iter, last_epoch=-1):
        self.end_lr = end_lr
        self.num_iter = num_iter
        super(ExponentialLR, self).__init__(optimizer, last_epoch)

    def get_lr(self):
        curr_iter = self.last_epoch + 1
        r = curr_iter / self.num_iter
        return [base_lr * (self.end_lr / base_lr) ** r for base_lr in self.base_lrs]
 
            
# Wrapper to iterate dataloader and provide an option to reset when StopIteration is called.
class DataLoaderIterWrapper(object):
    """
    Wrapper to iterate dataloader and provide labels and inputs. Provides functionality to stop in case of divergence (when StopIteration is called.)
    """
    def __init__(self, data_loader, auto_reset=True):
        self.data_loader = data_loader
        self.auto_reset = auto_reset
        self._iterator = iter(data_loader)
    
    # get new batchsize worth inputs and labels     
    def __next__(self):
        try:
            inputs, labels = next(self._iterator)
        except StopIteration:
            if not self.auto_reset:
                raise
            self._iterator = iter(self.data_loader)
            inputs, labels, *_ = next(self._iterator)
        return inputs, labels 
        
    def get_batch(self):
        return next(self)

class StateCacher(object):
    def __init__(self, in_memory, cache_dir=None):
        self.in_memory = in_memory
        self.cache_dir = cache_dir

        if self.cache_dir is None:
            import tempfile

            self.cache_dir = tempfile.gettempdir()
        else:
            if not os.path.isdir(self.cache_dir):
                raise ValueError("Given `cache_dir` is not a valid directory.")

        self.cached = {}

    def store(self, key, state_dict):
        if self.in_memory:
            self.cached.update({key: copy.deepcopy(state_dict)})
        else:
            fn = os.path.join(self.cache_dir, "state_{}_{}.pt".format(key, id(self)))
            self.cached.update({key: fn})
            torch.save(state_dict, fn)

    def retrieve(self, key):
        if key not in self.cached:
            raise KeyError("Target {} was not cached.".format(key))

        if self.in_memory:
            return self.cached.get(key)
        else:
            fn = self.cached.get(key)
            if not os.path.exists(fn):
                raise RuntimeError(
                    "Failed to load state in {}. File doesn't exist anymore.".format(fn)
                )
            state_dict = torch.load(fn, map_location=lambda storage, location: storage)
            return state_dict

    def __del__(self):
        """Check whether there are unused cached files existing in `cache_dir` before
        this instance being destroyed."""

        if self.in_memory:
            return

        for k in self.cached:
            if os.path.exists(self.cached[k]):
                os.remove(self.cached[k])
    