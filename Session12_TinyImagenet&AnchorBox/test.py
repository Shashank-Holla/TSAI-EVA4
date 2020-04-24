import torch
def test(net, device, testloader, criterion): 
    correct = 0
    total = 0
    epoch_test_loss = 0.0
    epoch_test_accuracy = 0
    net.eval()
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            images = images.to(device)
            labels = labels.to(device)
            outputs = net(images)

            epoch_test_loss += criterion(outputs, labels).item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
    epoch_test_accuracy = (100 * correct / total)
    epoch_test_loss /= len(testloader)
    # print("Test loss=",epoch_test_loss)
    # print('Accuracy of the network on the 10000 test images: %d %%' %epoch_test_accuracy)
    print('Epoch Test loss: {:.4f}, Epoch Test Accuracy: ({}/{}) - {:.2f}%'.format(epoch_test_loss, correct, total, epoch_test_accuracy))
    
    return epoch_test_accuracy, epoch_test_loss