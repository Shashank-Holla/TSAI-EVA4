# Tiny Imagenet and Object Localization

## PART A

Resnet18 on TinyImagenet

Train Resnet18 model on TinyImagenet dataset (with shuffled data in the ratio 70:30 for train and test images) and achieve test accuracy of atleast 50%.

**Run results** - Model achieved test accuracy of 56.3% in 48 epochs.

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

Find the optimal number of anchor boxes for custom dataset of 50 images of dogs.

Dataset of the images of dogs can be found here- [Dataset of images of dogs](https://github.com/Shashank-Holla/TSAI-EVA4/tree/master/Session12_TinyImagenet%26AnchorBox/ObjectLocalization/Dogs)

JSON file of the bounding box annotations can be found here- [BBox annotations](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session12_TinyImagenet%26AnchorBox/ObjectLocalization/dog_boundingbox_export_coco.json)

The main objects of the json file are:
1. **images** - contains details of each image checked for bounding box calculation. Details such as image file name, ID assigned, height and width of the uploaded image are present.

For example- first dog image has file name- 0.jpg and ID=0. The image has height and width of 375 and 500 pixels respectively.

2. **annotations** - annotations contain details for each object detected. If multiple objects are detected in a single image, then annotation details are captured for each of the objects. Annotation details contains id of the object, image id of the image where object was detected, category and bounding box details of each object. Bounding box include details such as top left x and y co-ordinate of the bounding box (housing the object), height and width of the bounding box.

    For example- Image name- 7.jpg has 2 objects (cat and dog detected) and details for each object is available. For the dog object's bounding box, the top left x and top left y co-ordinates are at 5 and 32 respectively.Width and height of the bounding box is 142 and 227.

3. **Categories**  - The categories object contains a list of categories (dog, cat) and each of those belongs to a supercategory. 

## Bounding box details

Height versus width trend for object's bounding boxes.

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session12_TinyImagenet%26AnchorBox/run_results/BoundingBox.JPG)

## Find optimum bounding boxes

Using elbow method (to determine the optimal number of clusters in k-means clustering), optimum number of cluster is found to be 3.

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session12_TinyImagenet%26AnchorBox/run_results/optimumclusters.JPG)


## Optimum Anchor box on bounding box distribution

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session12_TinyImagenet%26AnchorBox/run_results/clusters.JPG)
