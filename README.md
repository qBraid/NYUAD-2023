# NYUAD Hackathon for Social Good in the Arab World: Focusing on Quantum Computing (QC) and UN Sustainable Development Goals (SDGs).

https://nyuad.nyu.edu/en/events/2022/march/nyuad-hackathon-event.html

## Technical challenge

_Create a program that applies one or more quantum algorithms to a social good
problem of your choice._

**Quantum algorithm examples**:

- Shor's algorithm
- Grover's search
- Variational Quantum Eigensolver (VQE)
- Quantum Approximate Optimization Algorithm (QAOA)

---

<p align="center">
  <img width="460" height="460" src="https://github.com/qcswat/qatrah/blob/main/WDN%20animation.gif">
</p>

## Replacing Classical Pressure Sensors with Optimized Quantum Sensors

Compared to classical pressure sensors, quantum sensors are not invasive. They are also tolerant to the changes in the environment around it while also being more accurate. This improves the ability to detect pipe leakage.

## Leak Detection and Localization

### Using Quantum Machine Learning
Existing classical literature, suggests the use of machine learning to predict leakage and localise it to a particular pipe using the data from pressure sensors in the WDN at any given point of time. We attempt to solve the same using a quantum machine learning based model. 

Specifically, we collect the pressure data from the optimally-placed sensors in a water distribution network to predict leakage in the WDN using a quantum neural network. It is implemented in the Pennylane framework using Jax. The data is fed into the model using Angle encoding. The model is composed of a parametrised quantum circuit with RY, RZ and CNOT gates which are trained over a total of 500 epochs. We use a train to test-set ratio of 4:1 and optimise the model using Rectified adam over the binary cross-entropy loss. At the end we obtain a test accuracy of 87.02% over the dataset of size 650.
