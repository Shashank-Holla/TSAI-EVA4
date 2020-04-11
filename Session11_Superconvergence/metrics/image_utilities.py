import torch
import numpy as np
import torchvision
from torchvision.transforms import ToTensor

def capture_correct_incorrect_classified_samples(net, device, testloader):
    """
    Captures incorrect sample data- such as labels, predictions and images
    Input
        net - model
        device - device to run the model
        testloader - testloader
    """
    net.eval()
    incorrect_labels = torch.tensor([], dtype = torch.long)
    incorrect_predictions = torch.tensor([], dtype = torch.long)
    incorrect_images = torch.tensor([])

    # correct_labels = torch.tensor([], dtype = torch.long)
    # correct_predictions = torch.tensor([], dtype = torch.long)

    with torch.no_grad():
        for data in testloader:
            images, labels = data
            images = images.to(device)
            labels = labels.to(device)
            outputs = net(images)
            
            _, predicted = torch.max(outputs.data, 1)
            result = predicted.eq(labels.view_as(predicted))

            # Incorrect labels, images and predictions           
            incorrect_labels = torch.cat((incorrect_labels,labels[~result].cpu()), dim=0)
            incorrect_predictions = torch.cat((incorrect_predictions, predicted[~result].cpu()), dim=0)
            incorrect_images = torch.cat((incorrect_images, images[~result].cpu()), dim=0)
            # correct_labels = torch.cat((correct_labels,labels[result].cpu()), dim=0)
        
        return incorrect_labels.numpy(), incorrect_predictions.numpy(), incorrect_images



def dataset_calculate_mean_std():
        """
        Download train and test dataset, concatenate and calculate mean and standard deviation for this set.
        """
        set1 = torchvision.datasets.CIFAR10('./data', train=True, download=True, transform=ToTensor())
        set2 = torchvision.datasets.CIFAR10('./data', train=False, download=True, transform=ToTensor())
        data = np.concatenate([set1.data, set2.data], axis=0)
        stddev = list(np.std(data, axis=(0, 1, 2)) / 255)
        means = list(np.mean(data, axis=(0, 1, 2)) / 255)
        return stddev, means