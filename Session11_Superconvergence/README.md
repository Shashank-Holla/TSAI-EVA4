# Superconvergence

This is to implement the following changes-

1. Mixed Resnet model - a new resnet architecture with Convolution+Maxpool in every layer and resnet blocks in alternate layers.

2. One Cycle policy- a learning technique where the learning rate goes from lower learning rate (1/5th or 1/10th of the max learning rate) to higher learning rate in one half of the cycle. In the second half of the cycle, the model's LR comes back to the lower learning rate.

The motivation behind this is that, during the middle of learning when the learning rate is higher, the learning rate
works as a regularisation method and keep the network from overfitting. This helps the network to avoid steep areas
of loss and land better flatter minima.

3. Add image augmentation- a) Image padding  b) RandomCrop  c) HorizontalFlip  d) Cutout  


## Model parameters and hyperparameters

Learning rate boundaries : min LR=0.0038 max LR=0.038 (found from LR range test)

Optimizer : SGD

Loss function: Cross Entropy loss

Batch size = 512

Epochs = 24

One Cycle Policy

- min LR = 0.0038

- max LR = 0.038

- Steps per epoch = 98

- Epochs to reach max LR = 5



## Triangular LR Policy

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session11_Superconvergence/imgs/CyclicTriangle.JPG)


## Training and Validation loss/accuracy trend

Loss/Accuracy trend for train and test over training epochs.

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session11_Superconvergence/imgs/TrainTestAccLoss.JPG)

