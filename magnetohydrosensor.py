"""
This code was taken from https://qml.baidu.com/tutorials/quantum-simulation/variational-quantum-metrology.html#2-variational-quantum-sensors
we've modifide it by adding a class called MagnetoHydroSensor that takes as input the number of sensors and added a method to the class that take
in a list of magnetic fields that are used to calibrate the sensor to increase it's sensitvity.
"""

import numpy as np
from math import exp, pi
import matplotlib.pyplot as plt
from typing import Optional, Tuple, List
import paddle
import paddle_quantum as pq
from paddle_quantum.ansatz import Circuit
from paddle_quantum.loss import Measure

N = 2  # The number of qubits
depth_EN = 3  # The depth of encoding circuit
depth_DE = 3  # The depth of decoding circuit
LR = 0.2  # Learning rate
ITR = 150   # The number of optimization iterations
pq.set_backend('state_vector')
pq.set_dtype('complex128')

def RamseyCircuit(theta_EN: paddle.Tensor, theta_DE: paddle.Tensor, input_phi: float) -> Circuit:
    r""" Construct variational Ramsey interferometer
    
    Args:
        theta_EN: the parameters of encoding circuit, shape is [depth_En, num_qubits，3]
        theta_DE: the parameters of decoding circui, shape is [depth_De, num_qubits，3]
        input_phi: unknown parameter
    
    Returns:
        Circuit
    
    """
    depth_EN, depth_DE = theta_EN.shape[0], theta_DE.shape[0]
    num_qubits = theta_EN.shape[1]
    
    cir = Circuit(num_qubits)
    cir.ry(param=pi/2)
    
    # Construct the encoding circuit to generate an entangled state
    for depth in range(depth_EN):
        cir.u3(param=theta_EN[depth])
        cir.cnot()
    
    # the gate of unknown parameter
    cir.rz(param=input_phi)
    
    # Construct the decoding circuit to rotate the measurement basis
    for depth in range(depth_DE):
        cir.cnot()
        cir.u3(param=theta_DE[depth])
        
    cir.rx(param=pi/2)
    
    return cir

# Define the function to calculate m
def calculate_m(num_qubits: int)-> List[int]:
    m_list = []
    for k in range(2**num_qubits):
        k_bin = list(bin(k)[2:].zfill(num_qubits))
        u = k_bin.count('1')
        v = k_bin.count('0')
        m = u - v
        m_list.append(m)

    return m_list


def MSE(qnn: paddle.nn.Layer, phi: float) -> paddle.Tensor:
    r""" Calculate MSE 
    
    Args:
        cir: variational Ramsey interferometer
        phi: unknown parameter
        a: parameter of the estimator
        
    Returns:
        MSE
    
    """
    cir = RamseyCircuit(qnn.theta_EN, qnn.theta_DE, phi)
    
    # Measurement
    output_state = cir()
    prob = Measure()(output_state)
    
    num_qubits = cir.num_qubits
    m = calculate_m(num_qubits)
    return sum([((phi - qnn.a * m[i]) ** 2) * prob[i] for i in range(2 ** num_qubits)])


def std_mean(numbers):
    """
    This function takes a list of numbers as input and returns their mean.
    """
    return sum(numbers) / len(numbers)


def std_dev(numbers):
    """
    This function takes a list of numbers as input and returns their standard deviation.
    """
    n = len(numbers)
    if n <= 1:
        return 0.0
    avg = std_mean(numbers)
    variance = sum((x - avg) ** 2 for x in numbers) / (n - 1)
    return variance ** 0.5
# Define loss function
def loss_func(qnn: paddle.nn.Layer, magnetic_fields_list :list): #sampling_times: int, mean: float, variance: float):
    r""" Calculate loss 

    
    Args:
        qnn: a QNN
        sampling_times: the number of partitions in the selected interval
        mean: the mean of a normal distribution
        variance: the variance of a normal distribution
    
    """

    mean = std_mean(magnetic_fields_list)
    variance = std_dev(magnetic_fields_list)

    sampling_times = len(magnetic_fields_list)
    list_pdf = [] # The list of the probability density function of phi
    for phi in magnetic_fields_list:
        prob = (1 / (((2 * pi) ** 0.5) * variance)) * exp(-((phi - mean) ** 2) / (2 * (variance**2)))  # The probability density of phi
        list_pdf.append(prob)
    
    return sum([list_pdf[i] * MSE(qnn, magnetic_fields_list[i]) * (2 / sampling_times) for i in range(sampling_times)])

def optimization(qnn: paddle.nn.Layer, fields_list, num_itr: int, learning_rate: float) -> None:
    r""" Optimize QNN
    
    Args:
        qnn: a QNN
        num_itr: the number of optimization iterations
        learning_rate: learning rate
    
    """
    opt = paddle.optimizer.Adam(learning_rate=learning_rate, parameters=qnn.parameters())
    print("Begin：")
    for itr in range(1, num_itr):
        loss = qnn(fields_list)
        loss.backward()
        opt.minimize(loss)
        opt.clear_grad()

        if itr % 10 == 0:
            print("     iter:", itr, "loss:", "%.4f" % loss.numpy())

class RamseyInterferometer(paddle.nn.Layer):
    r""" Variational Ramsey interferometer
    
    """
    def __init__(self) -> None:
        super().__init__()
        
        # Add parameters
        theta_EN = self.create_parameter(
            shape= [depth_EN, N, 3], dtype="float64",
            default_initializer=paddle.nn.initializer.Uniform(low=0, high=2 * pi),
        )
        theta_DE = self.create_parameter(
            shape= [depth_DE, N, 3], dtype="float64",
            default_initializer=paddle.nn.initializer.Uniform(low=0, high=2 * pi),
        )
        self.add_parameter('theta_EN', theta_EN)
        self.add_parameter('theta_DE', theta_DE)
        
        # Add the parameter of the estimator
        a = self.create_parameter(
            shape= [1], dtype="float64",
            default_initializer=paddle.nn.initializer.Uniform(low=0, high=2 * pi),
        )
        self.add_parameter('a', a)
        
    def forward(self,fields_list) -> paddle.Tensor:
        r""" Calculate loss
        
        """
        return loss_func(self, fields_list)
    
    def opt(self,fields_list) -> None:
        r""" Optimize QNN
        
        """
        optimization(self,fields_list, num_itr=ITR, learning_rate=LR)



"""
phi_list = []
mse_list = []
for i in range(TIMES):
    phi = MEAN - 1 + (2 * i + 1) / TIMES
    mse_est = MSE(QNN, phi)
    phi_list.append(phi)
    mse_list.append(mse_est)"""



class MagnetoHydroSensor():
    def __init__(self,default_field=0, sensors_count=10):
        self.default_field = default_field

        sensors_fields = []
        self.QNN = RamseyInterferometer()


    def feedback_loop(self,sensors_fields):
        
        #self.QNN(sensors_fields)
        #self.optimize()
        self.QNN.opt(sensors_fields)
    #def optimize(self):
        
    def plot(self):
        font = {'family': 'Times New Roman', 'weight':'normal', 'size':16}
        plt.figure(dpi=100)
        plt.plot(phi_list,mse_list,color='darkblue', linestyle='-')
        plt.scatter(phi_list,mse_list)
        plt.xlabel('$\\phi$',font)
        plt.ylabel('MSE',font)

        plt.grid()
        #plt.show()
        return plt

        
sensor = MagnetoHydroSensor(10)
magnetic_fields = [4.4,5.3,4.3,9.8,6.5,3.9,5.3,4.2,5.1,5.8]
i = 0
iters = 14
while i < iters:
    sensor.feedback_loop(magnetic_fields)

