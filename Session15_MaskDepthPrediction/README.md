# Monocular Depth Estimation and Mask Prediction

Segmentation and Depth estimate are few key tasks in Computer Vision and are some of the fields where Deep Neural network really shines through. 
Image segmentation is to locate objects and their boundaries in an image. This mainly simplifies the representation of the image into something that is easier and meaningful to analyse, which is particularly useful in medical imaging and recognition tasks. Image segmentation involves creating pixel wise mask for the object in the image. 

Monocular Depth estimate is to gather perception of depth from a single static image. It provides information of how far things are relative to point of view.

The objective of this model is to predict the monocular depth map and also to create masks of the object of interest.


Model building is broken down into the following parts. We will work on the parts and then build the sum.


## Pre model training

- [X] - Dataset

- [X] - Data ingestion- Dataset and Dataloader

- [X] - Image augmentation


## Model Training

- [X] - Model Architecture

- [X] - Choose the Loss function

- [ ] - Model parameters and hyperparameters

- [ ] - Optimization



## Output of the model

- [ ] - Evaluating the output

- [ ] - Show data in Tensorboard

## Results and Observations

- [ ] - Run results

- [ ] - Observations

## TODO

## References
## Pre model training

### Dataset

Overlayed, mask and depth images considered this model are of Home interiors and cats as background and foreground respectively.

Dataset details can be found here - https://github.com/Shashank-Holla/TSAI-EVA4/tree/master/Session14_RCNN%26DenseDepth

### Data ingestion- Dataset and Dataloader

Custom dataset is built to read and provide a dictionary containing quartet of images- background image, background-foreground image, mask and depth image. The quartet of images are ensured to have the same context, that is, the same background and same location of the foreground in the images.

Find the code here.

### Image Augmentation

Image normalization and image resize have been applied. 
Earlier intention was to apply padding with border reflect and random crop to provide further augmented data and to apply RGB shift pixelwise transforms. Since random crop and probability based transforms are applied an image at a time, the context that is present in the quartet of images is lost. Therefore these have not been applied. 

As of now, probability based transform on pair of images without losing context is possible. It is shown here. Further understanding is required to apply transform in the same order and probability to the 4 images.

Transformation image here



## Model Training

### Model Architecture

To predict the depth and mask maps, the output of the model needs to be dense. That is, the prediction's resolution needs to be equal to that of the input. For this purpose, the model is designed with encoder-decoder architecture. Features of the input (edges, gradients, parts of the object) are extracted in the encoder segment. The decoder segment has two heads- one each to predict mask and depth maps.

#### Encoder
The encoder segment of the model consists of 4 encoder blocks. Each of the encoder blocks uses 3x3 regular convolution and 3x3 dilated convolution. Dilated convolution is used to capture the spatial information of the pixels. The result of these convolutions are concatenated. Further, the channel size is halved using 1x1 pointwise convolution.

#### Decoder
The decoder segment consists of 4 decoder blocks. The resolution of the feature maps are upscaled by a factor of 2 in each of the decoder blocks using pointwise convolution and pixel-shuffle. Pointwise convolution is here used to double the number of channels. Pixel-shuffle is later used to upscale the resolution.

The number of parameters used by the model is- 5,230,720. Forward/Backward pass size of the model is less than 500 MB making this a light model.


### Choose the Loss function

For mask segmentation prediction, (BCE + Dice) loss function is considered.

**BCE + Dice Loss**

Binary cross entropy loss provides large penalty when incorrect predictions are made with high probability. This is combined with Dice Loss (1-Dice Coefficient). Dice coefficient provides measure of overlap between the ground truth and the predicted output.

Code for the BCE+Dice loss can be found here- 


For depth map prediction, using just BCE+Dice loss gives result where the edges and contours of the background is lost. One result is shared below.

Hence, for depth predictions, SSIM and L1 loss is also considered.

**SSIM Loss** - Structural Similarity Index provides the perceptual difference between the ground truth depth map and the prediction. While, **L1 Loss** provides the absolute difference (numerical distance) between the ground truth and predicted image.



## Output of the model

### Evaluating the output

To evaluate the model, the following metrics are considered. Sigmoid of the prediction is taken before the metrics calculation as the ground truth of mask and depth map is in the range [0, 1].

**Dice Coefficient** - It measures to check the similarity by calculating the overlap between the two samples. Coefficient value ranges between 0 (no overlap) to 1 (highly similar).

**Mean Absolute Error** - It calculates the average of pixelwise numerical distance between the ground truth and prediction. Higher the metric, higher the error. 

**Root Mean Square Error** - It calculates the pixelwise root mean square between thr ground truth and prediction.


## References

### Pre model training

Dataset - https://stanford.edu/~shervine/blog/pytorch-how-to-generate-data-parallel

Image augmentation - https://github.com/albumentations-team/albumentations#how-to-use
                     https://github.com/albumentations-team/albumentations/pull/133

### Model Architecture

https://arxiv.org/abs/1904.03380
https://mc.ai/u-net-dilated-convolutions-and-large-convolution-kernels-in-deep-learning/
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6514714/

