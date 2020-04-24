import torch
import torchvision
import torchvision.transforms as transforms
from tqdm.autonotebook import tqdm

def train(net, device, trainloader, optimizer, criterion, epoch, scheduler=None):
    net.train()
    pbar = tqdm(trainloader)
    epoch_train_loss = 0.0
    epoch_train_accuracy = 0
    correct = 0
    processed = 0
    for i, data in enumerate(pbar, 0):
        # get the inputs. Data is not on cuda. Move it. Number of images, labels per iteration = batch size in transform
        inputs, labels = data
              
        inputs = inputs.to(device)
        labels = labels.to(device)

        # zero the parameter gradients
        optimizer.zero_grad() 

        # forward + backward + optimize
        
        outputs = net(inputs)
        loss = criterion(outputs, labels) #Loss calculation is on cuda
        loss.backward()
        optimizer.step()
        
        #Scheduler update. For one cycle policy, scheduler is to be updated after every batch.
        if scheduler:
            scheduler.step()

        #Accuracy calculation
        pred = outputs.argmax(dim=1, keepdim=True)
        correct += pred.eq(labels.view_as(pred)).sum().item()
        processed += len(inputs)
        
        epoch_train_loss += loss.item()
        pbar_details = f'Loss={loss.item():0.4f} -  Accuracy={100*correct/processed:0.2f}%'
        pbar.set_description(desc= pbar_details)


    # print("Number of correct",correct,"\nTotal:",processed)    
    epoch_train_accuracy=(100*correct/processed)
    # print("Accuracy=",epoch_train_accuracy)
    epoch_train_loss /= len(trainloader)
    
    # print("Total loss for epoch: ",i, "is", epoch_train_loss)

    print('Epoch train loss: {:.4f}, Epoch Train Accuracy: {:.2f}%'.format(epoch_train_loss, epoch_train_accuracy))
    
    return epoch_train_accuracy, epoch_train_loss