# Training and Learning rates

This is to implement the following Learning techniques to train the model.

1.  Implement LR finder- a method to estimate reasonable minimum and maximum boundary values with one training run of the network for a few epochs. (Ref- https://arxiv.org/abs/1506.01186)

2.  Implement Reduce LR on plateau- a method to reduce LR once learning stagnates.

3.  Also, to find the the network's focus area on the image (using GRADCAM) when misclassifying the images. 

## Model parameters and hyperparameters

- LR finder : start_lr = 0.001 and end_lr=0.01 (linear): Steep decrease in loss observed between 0.003 and 0.006

- Optimizer : SGD with momentum (0.9). Learning rate = 0.04 
              ReduceLRonPlateau : factor=0.1, patience=2
              
- Epochs : 50

## LR Finder
1. start_lr=0.001 and end_lr=0.05 (exp): Steep decrease in loss observed between 0.001 and 0.01

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session10_LearningRate/imgs/LRfind_run1_exp.JPG)

2. start_lr = 0.001 and end_lr=0.01 (linear): Steep decrease in loss observed between 0.003 and 0.006. LR

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session10_LearningRate/imgs/LRfind_run2_linear.JPG)


## Test results

Train/Test loss and accuracy trend against epoch.


## GradCAM

GradCAM test results for missclassified images.
