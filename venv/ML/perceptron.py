import numpy as np
import matplotlib.pylab as plt

def sigmoid(x):
    return  1/(1 + np.exp(-x))
def sigmoid_derivative(x):
    return x *(1-x)


def relu(x):
    return np.maximum(0,x)



training_input= np.array([[0,1,1],[1,1,1],[1,1,1],[0,1,1]])

training_output = np.array([[1,1,1,1]]).T

np.random.seed(1)

synaptic_weights = 2* np.random.random((3,1))-1
print ('Random synaptic wieghts:',synaptic_weights)

for it in range(500000):
    input_layer = training_input

    outputs = sigmoid(np.dot(input_layer, synaptic_weights))
    outputs1 = relu(np.dot(input_layer, synaptic_weights))

    error = training_output - outputs
    adjustments = error * sigmoid_derivative(outputs)
    synaptic_weights += np.dot(input_layer.T, adjustments)

print('Synaptic weights after training:\n', synaptic_weights)
print ('Outputs sigmoid after training:\n',outputs)
print ('Outputs relu after training:\n',outputs)
# x = np.arange(-10.0,10.0,0.1)
# y1 = relu(x)
# y2 = sigmoid(x)
# plt.plot(x,y1)
# plt.ylim(-1,6.0)
#
# plt.plot(x,y2)
# plt.ylim(-1,6.0)
# plt.show()

