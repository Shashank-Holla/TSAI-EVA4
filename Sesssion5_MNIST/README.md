File - EVA4_S5_F1_BasicStructure
Target:

Get the basic code structure. This is from previous submission. (Dropout used after every 2 convolution layers. BatchNorm not used in later convolutions. No GAP used.)

Results:

Number of parameters: 20026
Training accuracy : 99.21%
Testing accuracy : 99.39%
Analysis:

No overfitting. Test accuracy is a bit better than training accuracy. Shows model is trained harder.
But accuracy is not hitting high accuracy under 15 epoch (99.4%).
Number of parameters used in higher than desired. (20K > 10K required).
