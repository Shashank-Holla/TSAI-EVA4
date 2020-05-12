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

| Image Type | No of Images | Total Imageset Size | Mean | Std. Dev |
|------------|--------------|---------------------|------|----------|
| fg         | 100          |                     |      |          |
| bg         | 100          |                     |      |          |
| fg_bg      | 400000       |                     |      |          |
| mask       | 400000       |                     |      |          |
| depth      | 400000       |                     |      |          |



