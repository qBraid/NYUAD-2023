import numpy as np
import pandas as pd
import haiku as hk
import jax
import optax
from sklearn.metrics import accuracy_score
import pennylane as qml
from pennylane import numpy as np
import jax
from jax import random
import haiku as hk

# Load data
x_train = pd.read_excel("x_train.xlsx")
y_train = pd.read_excel("y_train.xlsx")
x_test = pd.read_excel("x_test.xlsx")
y_test = pd.read_excel("y_test.xlsx")

n_qubits = 8
epochs = 500
batch_size = 32
num_layers = 8

num_batches = len(x_train) // batch_size
dev = qml.device("default.qubit", wires=n_qubits)

def quantum_layer(weights):
    qml.templates.AngleEmbedding(weights[:, 0], rotation="Y", wires=range(n_qubits))
    qml.templates.AngleEmbedding(weights[:, 1], rotation="Z", wires=range(n_qubits))
    for i in range(8):
        qml.CNOT(wires=[i, (i + 1) % 8])

@qml.qnode(dev, interface="jax")
def quantum_circuit(x, circuit_weights):
    for weights in circuit_weights:
        qml.templates.AngleEmbedding(x, wires=range(n_qubits))
        quantum_layer(weights)
    return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]


@hk.without_apply_rng
@hk.transform
def qforward(x):
    x = jax.nn.tanh(hk.Linear(8)(x))
    W = hk.get_parameter(
        "W", (num_layers, 8, 3), init=hk.initializers.RandomNormal(stddev=0.25)
    )
    x = jax.vmap(quantum_circuit, in_axes=(0, None))(x, W)
    x = hk.Linear(1)(x)
    return x

@hk.without_apply_rng
@hk.transform
def cforward(x):
    nn = hk.Sequential([hk.Linear(10), 
                       jax.nn.relu,
                       hk.Linear(10), 
                       jax.nn.relu,
                       hk.Linear(1)])
    return nn(x)

seed = 123
rng = jax.random.PRNGKey(seed)
params = qforward.init(rng, x_train.values)
opt = optax.radam(learning_rate=5e-4)
opt_state = opt.init(params)

# Training loop
def loss_fn(params, x, y):
    pred = qforward.apply(params, x)
    loss = optax.sigmoid_binary_cross_entropy(pred, y).mean()
    return loss


@jax.jit
def update(params, opt_state, x, y):
    loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
    updates, new_opt_state = opt.update(grads, opt_state)
    new_params = optax.apply_updates(params, updates)
    return new_params, new_opt_state, loss

loss_list = []
test_acc = []
for epoch in range(epochs):
    # Shuffle the training data
    shuffled_indices = np.random.permutation(len(x_train))
    x_train_shuffled = x_train.values[shuffled_indices]
    y_train_shuffled = y_train.values[shuffled_indices]

    # Training
    epoch_loss = 0
    for batch_idx in range(num_batches):
        start = batch_idx * batch_size
        end = start + batch_size

        x_batch = x_train_shuffled[start:end]
        y_batch = y_train_shuffled[start:end]

        params, opt_state, batch_loss = update(params, opt_state, x_batch, y_batch)
        epoch_loss += batch_loss

    epoch_loss /= num_batches
    loss_list.append(epoch_loss)

    # Testing
    y_pred = qforward.apply(params, x_test.values)
    y_pred_labels = (y_pred > 0.5).astype(int)
    test_accuracy = accuracy_score(y_test, y_pred_labels)
    print(
        f"Epoch {epoch + 1}, Loss: {epoch_loss:.4f}"
    )
    test_acc.append(test_accuracy)

# Testing
y_pred = qforward.apply(params, x_test.values)
y_pred_labels = (y_pred > 0.5).astype(int)
test_accuracy = accuracy_score(y_test.values, y_pred_labels)
print(f"Test Accuracy: {test_accuracy:.4f}")