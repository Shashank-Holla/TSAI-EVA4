# Monocular Depth Estimation and Mask Prediction

Segmentation and Depth estimate are few key tasks in Computer Vision and are some of the fields where Deep Neural network really shines through. 
Image segmentation is to locate objects and their boundaries in an image. This mainly simplifies the representation of the image into something that is easier and meaningful to analyse, which is particularly useful in medical imaging and recognition tasks. Image segmentation involves creating pixel wise mask for the object in the image. 

Monocular Depth estimate is to gather perception of depth from a single static image. It provides information of how far things are relative to point of view.

The objective of this model is to predict the monocular depth map and also to create masks of the object of interest.


Model building is broken down into the following parts. We will work on the parts and then build the sum.


## Pre model training


- [X] - Data ingestion- Dataset and Dataloader

- [ ] - Image augmentation


## Model Training

- [ ] - Model Architecture

- [ ] - Choose the Loss function



## Output of the model

- [ ] - How is the output presented

- [ ] - Show data in Tensorboard


### Data ingestion- Dataset and Dataloader

### Image Augmentation

### Model Architecture

To predict the depth and mask maps, the output of the model needs to be dense. That is, the prediction's resolution needs to be equal to that of the input. For this purpose, the model is designed with encoder-decoder architecture. Features of the input (edges, gradients, parts of the object) are extracted in the encoder segment. The decoder segment has two heads- one each to predict mask and depth maps.

#### Encoder
The encoder segment of the model consists of 4 encoder blocks. Each of the encoder blocks uses 3x3 regular convolution and 3x3 dilated convolution. Dilated convolution is used to capture the spatial information of the pixels. The result of these convolutions are concatenated. Further, the channel size is halved using 1x1 pointwise convolution.

#### Decoder
The decoder segment consists of 4 decoder blocks. The resolution of the feature maps are upscaled by a factor of 2 in each of the decoder blocks using pointwise convolution and pixel-shuffle. Pointwise convolution is here used to double the number of channels. Pixel-shuffle is later used to upscale the resolution.

The number of parameters used by the model is- 5,230,720. Forward/Backward pass size of the model is less than 500 MB making this a light model.

#### Choose the Loss function
