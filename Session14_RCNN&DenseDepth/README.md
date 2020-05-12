# Dataset Preparation for Monocular Depth Estimation and Segmentation

Objective: This is to prepare custom dataset for Monocular Depth estimation and segmentation model.

The prepared dataset includes depth and mask images of foreground objects overlayed on background images. Depth images contain information about the distance between the surface of objects from a given viewpoint. 

Link to the Dataset - [MonocularDepth_Mask_Dataset](https://drive.google.com/drive/folders/1ACsG-epUmRCJ0zaKIAGGc5DzeG3SSY65)


## Custom Dataset

* **Background Images (bg)** - Square shaped "Scene" images.
* **Foreground Images (fg)** - Images of objects of interest.
* **Overlayed Images (bg_fg)** - Images of foreground objects overlayed on background images at random locations. Foreground images are also flipped and overlayed on the background.
* **Mask Images (mask)** - Mask of the overlayed foreground-background images.
* **Depth Images (depth)** - Depth maps of foreground-background images.

Schrodinger's cat
Overlayed, mask and depth images are created considering Home interiors and cats as background and foreground respectively.


## Dataset Statistics

Below are the stats gathered for the dataset. Foreground images are scaled to a height of 80 while maintaining the aspect ratio.

| Image Type | No of Images | Image Dimension | Total Imageset Size | Mean | Std. Dev |
|------------|--------------|-----------------|---------------------|------|----------|
| fg         | 100          |  192 * 192      |                     |      |          |
| bg         | 100          |  x * 80         |                     |      |          |
| fg_bg      | 400000       |  192 * 192      |                     |      |          |
| mask       | 400000       |  192 * 192      |                     |      |          |
| depth      | 400000       |  192 * 192      |                     |      |          |


## Dataset Overview


## Dataset creation

### Background and Foreground images (bg and fg)

* 100 images of home interiors are collected from the web. The raw background images are cropped while maintaining 1:1 aspect ratio.     Further the background images are rescaled to 192 X 192 dimension.

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session14_RCNN%26DenseDepth/results/background_images.jpg)

* 100 images of cats are collected from the web. For the image overlay, the foreground images are scaled to a fixed height of 80 while maintaining the image's aspect ratio.

![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session14_RCNN%26DenseDepth/results/foreground_images.jpg)



### Creation of foreground images with transparency

For a clean overlay of the foreground image on background, the foreground images are required to have a transparent background. GIMP (GNU Image Manipulation Program) is used for this purpose. Steps are-

* For the image in GIMP, add Alpha channel to the image ( Layer -> Transparency -> Add Alpha channel ). Alpha channel value of 0 represents full transparency while the maximum value indicates opaqueness.

* Select the object in the image using Free Hand tool. Later, invert the selection and delete the background.

* Save the modified image as .png file to retain the alpha channel.


### Mask creation for the foreground





