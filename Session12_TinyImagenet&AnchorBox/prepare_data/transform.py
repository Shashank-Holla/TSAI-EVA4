import torch
import torchvision
import torchvision.transforms as transforms


def transform(means, stddev, batch_size):

    train_transforms = transforms.Compose(
       [
        # transforms.RandomCrop(32, padding=4),
       transforms.RandomHorizontalFlip(),
       transforms.ToTensor(),
       transforms.Normalize(means, stddev),
        transforms.RandomErasing(p=1, scale=(0.25, 0.25), ratio=(1, 1), value=means, inplace=False)
        ])
        
    test_transforms = transforms.Compose(
       [
       transforms.ToTensor(),
       transforms.Normalize(means, stddev)
        ])
    
    trainset = torchvision.datasets.ImageFolder(root='./train_folder', transform=train_transforms)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=8)

    testset = torchvision.datasets.ImageFolder(root='./test_folder', transform=test_transforms)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=8)

    

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