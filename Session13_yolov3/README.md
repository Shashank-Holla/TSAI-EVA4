# Object detection using YOLO v3

## PART A: Object detection using OpenCV YOLO v3

Objective: Detect objects in an image having person and items from COCO dataset. Object detection is done using YOLO v3 on OpenCV.

### Result
![](https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session13_yolov3/Images/shashank.jpg)




## PART B: Object detection using YOLO v3 on pytorch

Objective: Train YOLO v3 on custom dataset (objects that are not available on COCO dataset). 
Emmet Brickowski, a Lego minifigure character, is our protagonist for the object detection.


### Dataset preparation

Steps for the Training data preparation is as follows-

* Collect dataset of Emmet and annotate the bounding boxes using [Annotation tool](https://github.com/miki998/YoloV3_Annotation_Tool).
* Place the training image set in \data\customdata\images folder.
* Place the annotation files in \data\customdata\labels folder.
* Update custom.names file with the desired class name (Emmet in our case).
* Have the list of images for the network to be trained on in custom.txt


### Download pre-trained weights

Download pre-trained weights from (https://drive.google.com/open?id=1LezFG5g3BCW6iYaV89B2i64cqEUZD7e0) and place it in weights folder in the root YoloV3 folder.


### Training the model

To train the model on custom dataset, run the command

`!python train.py --data data/customdata/custom.data --batch 10 --cache --cfg cfg/yolov3-custom.cfg --epochs 200 --nosave`

### Inference on images

To infer on images (images from training set), run the command

`!python detect.py --conf-thres 0.1 --output out_out`

### Inference on video

For video inference, run the command

`!python detect.py --conf-thres 0.1 --output data/output_video --source data/input_video/input_video.mp4`

To prepare the final output video, follow the steps

* Extract audio from the original input video.

  `ffmpeg -i .\input_video.mp4 -c:a libmp3lame -q:a 4 input_sound.mp3`
  
* Merge audio with inferred video
 
  `ffmpeg -i .\output_video.mp4 -i .\input_sound.mp3 final_output.mp4`
  
* To cut part of the output video
 
  `ffmpeg -i .\final_output.mp4 -ss 00:00:32 -t 00:00:50 -async 1 -strict -2 cut_output.mp4`


### Results

Inference on images

<p>
<img src="https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session13_yolov3/Images/img001.jpg" alt="Emmet_1"
	title="Emmet_1" width="400" height="200" />
 <img src="https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session13_yolov3/Images/img012.jpg" alt="Emmet_2"
	title="Emmet_2" width="400" height="200" />
 </p>
 <p>
<img src="https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session13_yolov3/Images/img033.jpg" alt="Emmet_3"
	title="Emmet_3" width="400" height="200" />
 <img src="https://github.com/Shashank-Holla/TSAI-EVA4/blob/master/Session13_yolov3/Images/img076.jpg" alt="Emmet_4"
	title="Emmet_4" width="400" height="200" />
 </p>
 
 Inference on video
 
 [![](https://www.youtube.com/watch?v=ZePHNqliwPc/0.jpg)](https://www.youtube.com/watch?v=ZePHNqliwPc)
  

