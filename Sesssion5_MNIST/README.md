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


File- EVA4_S5_F2_SkeletalModel&BatchNorm

Target:

As previous model was over 20K, make the model lighter. Also added BatchNorm after every convolution to increase model efficiency.

Results:

Number of parameters: 6.6K
Training accuracy : 98.85%
Testing accuracy : 99.22%
Analysis:

Very light model. Scope to improve.
No overfitting. Test accuracy is a bit better than training accuracy. Shows model is trained harder. But model is not hitting required accuracy of 99.4%.


File- EVA4_S5_F3_AdditionalConvLayers

Target:

As previous model was well below capacity and accuracy was not hitting 99.4%, added additional convolution layers to increase capacity.

Results:

Number of parameters: 11.3K
Training accuracy : 99.14%
Testing accuracy : 99.32%
Analysis:

Test accuracy is still not achieving desired value. Model is not showing any overfitting. Shows model is trained harder.


File- EVA4_S5_F4_GAPLayer

Target:

Convolution layer was being used as the last layer. Use GAP to reduce the last big layer. Since model's capacity is reduced, add another convolution block after GAP to increase capacity.

Results:

Number of parameters: 9.5K
Training accuracy : 98.92%
Testing accuracy : 99.15%
Analysis:

Test accuracy is still not achieving desired value. Model is not showing any overfitting. Shows model is trained harder.

