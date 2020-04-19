import torch
import torchvision

from PIL import Image
import cv2
import numpy as np
import torchvision

#pip is executed in the main file.
# import pip
# !pip install -U git+https://github.com/albu/albumentations --no-cache-dir

import albumentations
print('Albumentations version:',albumentations.__version__)
from albumentations import Compose, Normalize, HorizontalFlip, Resize, RandomBrightnessContrast, Cutout, CoarseDropout, GaussNoise, PadIfNeeded, RandomCrop
from albumentations.pytorch import ToTensor

class album_compose:
    def __init__(self, settype):
        self.settype = settype
        self.stddev, self.means = self.dataset_calculate_mean_std()
        if self.settype == 'train':
          print("Train set")
          self.albumentation_transform = Compose([
                # PadIfNeeded(min_height=40, min_width=40, border_mode=1, value=list(255 * self.means), p=1.0),  
                #   RandomBrightnessContrast(always_apply=False, p=0.5, brightness_limit=(-0.40, 0.82), contrast_limit=(-0.40, 0.82), brightness_by_max=True),
                RandomCrop(height=32, width=32, always_apply=True, p=1.0),
                HorizontalFlip(always_apply=True, p=1.0),
                Cutout(always_apply=True, p=1.0, num_holes=1, max_h_size=8, max_w_size=8, fill_value=list(255 * self.means)),
                #   GaussNoise(always_apply=False, p=1.0, var_limit=(60, 100)),
                #   CoarseDropout(max_holes=2, max_height=16, max_width=16, min_holes=1, min_height=8, min_width=8, fill_value=list(255 * self.means), always_apply=False, p=1.0),
                  Normalize(
                      mean = list(self.means),
                      std = list(self.stddev),
                      ),
                  ToTensor()
          ])
        elif self.settype == 'test':
          print("Test set")
          self.albumentation_transform = Compose([
                  Normalize(
                      mean = list(self.means),
                      std = list(self.stddev),
                  ),
                  ToTensor()
          ])
    
    def dataset_calculate_mean_std(self):
        """
        Download train and test dataset, concatenate and calculate mean and standard deviation for this set.
        """
        set1 = torchvision.datasets.CIFAR10('./data', train=True, download=True, transform=ToTensor())
        set2 = torchvision.datasets.CIFAR10('./data', train=False, download=True, transform=ToTensor())
        data = np.concatenate([set1.data, set2.data], axis=0)
        stddev = (np.std(data, axis=(0, 1, 2)) / 255)
        means = (np.mean(data, axis=(0, 1, 2)) / 255)
        return stddev, means
        
    def __call__(self, img):
        img = np.array(img)
        img = self.albumentation_transform(image=img)['image']
        return img
    
def transform(batch_size):
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=album_compose('train'))
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=8)

    testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=album_compose('test'))
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=8)

    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
    return trainloader, testloader, classes