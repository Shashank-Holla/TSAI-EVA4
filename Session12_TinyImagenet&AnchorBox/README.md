# Tiny Imagenet and Object Localization

## PART A

Resnet18 on TinyImagenet

Train Resnet18 model on TinyImagenet dataset (with shuffled data in the ratio 70:30 for train and test images) and achieve test accuracy of atleast 50%.

Model achieved test accuracy of 56.3%

### Model parameters and hyperparameters

- Optimizer : SGD
- Loss function: Cross Entropy loss
- Batch size = 256
- Epochs = 48
- L2 Regularization = 0.01

One Cycle Policy
- min LR = 0.001
- max LR = 0.01
- div_factor = 100
- Epochs to reach max LR = 8

### Image Augmentation applied

- Padding on all sides by 8 followed by random crop of 64
- Horizontal flip (50% probability)
- Rotate upto [-15, 15 degrees] (50% probability).
- Gaussian noise and coarse dropout of size [8, 16].

### Training and Validation loss/accuracy trend
![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session12_TinyImagenet%26AnchorBox/run_results/TrainTest_graphs.JPG)

### Activation mapping for misclassified images

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session12_TinyImagenet%26AnchorBox/run_results/grad_cam_missclassified.jpg)


## PART B
Object Localization
