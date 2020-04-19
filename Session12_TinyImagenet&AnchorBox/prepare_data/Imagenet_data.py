import torch
import numpy as np
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import glob
from shutil import move, rmtree
import time
import random
import os
from tqdm.autonotebook import tqdm
import requests
import zipfile
from io import BytesIO



def imagenet_download_and_extract():
    """
    Function will 
        1. create data folder in virtual machine's /content folder where Tiny Imagenet will be stored.
        2. Download Tiny Imagenet from http://cs231n.stanford.edu/tiny-imagenet-200.zip
        3. Unzip Image set.

    """
    if not os.path.exists("data"):
        print("data folder for Imagenet is being created.")
        os.mkdir("data")

    os.chdir("data")
    zip_file_name = "tiny-imagenet-200.zip"
    file_name = "tiny-imagenet-200"
    URL = "http://cs231n.stanford.edu/tiny-imagenet-200.zip"

    if (os.path.isfile(zip_file_name)):
        print("Imagenet file exists")
    else:
        print("\nImagenet dataset does not exist. Downloading...\n")
        tic = time.time()
        r = requests.get(URL, stream=True)
        print("\nFile downloaded. Unzipping file.\n")
        zip_ref = zipfile.ZipFile(BytesIO(r.content))
        zip_ref.extractall('./')
        zip_ref.close()
        toc = time.time()
        print("\nFile unzip completed. Time taken- {:.2f} sec".format((toc-tic)))
		

def train_validation_dataset_merge():
    """
    Function will move images from validation folder into train folder.
    In case a particular class file is not found in train, new folder will be created.
    """
    #Go to tiny-imagenet-200 folder.
    os.chdir("tiny-imagenet-200")
    target_folder = './val'
    dest_folder = './train'

    val_dict = {}
    print("Train and Validation dataset merge begins.")
    tic = time.time()
    with open(os.path.join(target_folder,'val_annotations.txt')) as fp:
        data = fp.readlines()
        for line in data:
            key, value = line.split('\t')[0:2]
            val_dict[key] = value

    paths = glob.glob(os.path.join(target_folder,'images/*'))
    for path in paths:
        file = path.split('/')[-1]
        folder = val_dict[file]
        if not os.path.exists(os.path.join(dest_folder,folder)):
            print("Folder {} does not exist in training set. New folder will be created".format(folder))
            os.mkdir(os.path.join(dest_folder,folder))
            os.mkdir(os.path.join(dest_folder, folder,"images"))
            
        dest = os.path.join(dest_folder,folder,"images",file)
        move(path, dest)
    toc = time.time()
    print("Train and Validation dataset merge is completed. Time taken-{:.2f} msec".format((toc-tic)*1000))  
	

def train_test_dataset_split(train_split_percentage = 0.7):
    """
    Function will split data present in train folder into train set (train_folder) and test set (test_folder) in the ratio as specified.
    Default train/test split = 70 : 30
    
    """

    if os.path.exists("train_folder"):
        rmtree("train_folder")
    if os.path.exists("test_folder"):
        rmtree("test_folder")
    os.mkdir("test_folder")
    os.mkdir("train_folder")

    target_folder = './train'
    train_folder = './train_folder'
    test_folder = './test_folder'
     

    paths = glob.glob(os.path.join(target_folder,"*"))

    for path in tqdm(paths):
        folder = path.split('/')[-1].rstrip()
        images = glob.glob(os.path.join(target_folder,folder,"images/*"))
        class_dataset_size = len(images)
        train_dataset_size = int(np.floor(class_dataset_size * train_split_percentage))
        random.shuffle(images)
        train_images = images[:train_dataset_size]
        test_images = images[train_dataset_size:]

        # Folder creation and data copy for training set for one class.
        os.mkdir(os.path.join(train_folder,folder))
        os.mkdir(os.path.join(train_folder,folder,"images"))
        for image in train_images:
            move(image,os.path.join(train_folder,folder,"images"))

        # Folder creation and data copy for training set for one class.
        os.mkdir(os.path.join(test_folder,folder))
        os.mkdir(os.path.join(test_folder,folder,"images"))
        for image in test_images:
            move(image,os.path.join(test_folder,folder,"images"))
			
