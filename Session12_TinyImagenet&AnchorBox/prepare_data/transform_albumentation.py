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
from albumentations import Compose, Normalize, HorizontalFlip, Resize, RandomBrightnessContrast, Cutout, CoarseDropout, GaussNoise, PadIfNeeded, RandomCrop, Rotate
from albumentations.pytorch import ToTensor

class album_compose:
    def __init__(self, means, stddev, settype):
        self.settype = settype
        self.means = np.array(means)
        self.stddev = np.array(stddev)
        
        if self.settype == 'train':
          print("Train set")
          self.albumentation_transform = Compose([
                PadIfNeeded(min_height=72, min_width=72, border_mode=1, value=list(255 * self.means), p=1.0),  
                #   RandomBrightnessContrast(always_apply=False, p=0.5, brightness_limit=(-0.40, 0.82), contrast_limit=(-0.40, 0.82), brightness_by_max=True),
                RandomCrop(height=64, width=64, always_apply=True, p=1.0),
                HorizontalFlip(always_apply=False, p=0.5),
                Rotate(limit=15, interpolation=1, border_mode=4, value=None, mask_value=None, always_apply=False, p=0.5),
                # Cutout(always_apply=True, p=1.0, num_holes=1, max_h_size=8, max_w_size=8, fill_value=list(255 * self.means)),
                GaussNoise(always_apply=False, p=1.0, var_limit=(60, 100)),
                CoarseDropout(max_holes=1, max_height=16, max_width=16, min_holes=1, min_height=8, min_width=8, fill_value=list(255 * self.means), always_apply=False, p=1.0),
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
    
    def __call__(self, img):
        img = np.array(img)
        img = self.albumentation_transform(image=img)['image']
        return img
    
def transform(means, stddev, batch_size):
    trainset = torchvision.datasets.ImageFolder(root='./train_folder', transform=album_compose(means, stddev, 'train'))
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=16)

    testset = torchvision.datasets.ImageFolder(root='./test_folder', transform=album_compose(means, stddev, 'test'))
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=True, num_workers=16)
    
    
    
    
    def create_class_to_name_map():
        """
        # Create dictionary with name and class mapping for required classes.
        # File wnids.txt contains the 200 labels that are present in the train and validation set.
        # File words.txt contain the class's names.


        Output - class_to_name dictionary
        """

        # Prepare dictionary with all the required classes.
        class_to_name = dict()
        classes = []
        with open('wnids.txt', 'r') as fp:
            data = fp.readlines()
            for id in data:
                classes.append(id.strip('\n'))

        classes.sort()        

        #Extract names of all the classes.
        all_classes = dict()
        with open('words.txt','r') as fp:
            data = fp.readlines()

            #Map names to the class_to_name dictionary which contains the required classes.
            for line in data:
                words = line.strip('\n').split('\t')
                all_classes[words[0]] = words[1].split(',')[0]

            
        for i in range(len(classes)):
            name = all_classes[classes[i]]
            class_to_name[i] = (classes[i], name)


        return class_to_name
        

    classes = create_class_to_name_map()
    
    return trainloader, testloader, classes