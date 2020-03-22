# Training and Learning rates

This is to implement the following Learning techniques to train the model.

1.  Implement LR finder- a cyclical learning rate method to find the best LR.  Instead of monotonically decreasing the learning rate, this method lets the learning rate cyclically vary between reasonable boundary values. Training with cyclical learning rates instead of fixed values achieves improved classification accuracy without a need to tune and often in fewer iterations. (Ref- https://arxiv.org/abs/1506.01186)

2.  Implement Reduce LR on plateau- a method to reduce LR once learning stagnates.

3.  Also, to find the the network's focus area on the image (using GRADCAM) when misclassifying the images. 
