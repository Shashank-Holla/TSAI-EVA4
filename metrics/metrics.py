import matplotlib.pyplot as plt

def train_test_metrics_graph(train_accuracy, train_loss, test_accuracy, test_loss):
  
  fig, axs = plt.subplots(1,2,figsize=(15,7.5))
  axs[0].set_title("Accuracy")
  axs[0].plot(train_accuracy, label = "train_accuracy")
  axs[0].plot(test_accuracy, label = "test accuracy")
  axs[0].set_xlabel("Epoch")
  axs[0].set_ylabel("Accuracy")
  axs[0].legend(loc="best")

  axs[1].set_title("Loss")
  axs[1].plot(train_loss, label = "train loss")
  axs[1].plot(test_loss, label = "test loss")
  axs[1].set_xlabel("Epoch")
  axs[1].set_ylabel("Loss")
  axs[1].legend(loc="best")