import math

# ✅ Activation Functions
def relu(x):
    return [[max(0, i) for i in row] for row in x]

def softmax(x_batch, T=2):
    """Numerically stable softmax with temperature scaling."""
    return [[math.exp((i - max(row)) / T) / (sum(math.exp((j - max(row)) / T) for j in row) + 1e-9) for i in row] for row in x_batch]

# ✅ Proper Matrix Multiplication
def matmul(A, B):
    """Multiply two matrices A (m × n) and B (n × p) → returns (m × p)"""
    return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]

# ✅ Fully Connected Layer (Batch Processing)
def dense(x_batch, w, b, activation):
    output = matmul(x_batch, w)  # Matrix Multiplication
    output = [[o + bias for o, bias in zip(row, b)] for row in output]  # Add Bias

    if activation == "relu":
        return relu(output)
    elif activation == "softmax":
        return softmax(output, T=3)  # ✅ Temperature Scaling
    elif activation == "linear":
        return output 
    else:
        raise ValueError("Invalid activation function")

# ✅ Load Weights from File (SAFE METHOD)
def load_weights_from_file(filename):
    """Reads weights and biases from a file and assigns them to variables."""
    with open(filename, "r") as file:
        data = file.read()  # Read the file as a string

    weights = eval(data)  # ✅ Safer than eval()
    w1, b1, w2, b2, w3, b3 = [item for item in weights]  
    return w1, b1, w2, b2, w3, b3

# ✅ Load Pre-trained Weights
w1, b1, w2, b2, w3, b3 = load_weights_from_file("hyper_param.txt")

# ✅ Test Data: Temperature, Humidity, Pressure
Xtest = [[29.6, 69.45, 1001.9], [27.3, 92.01, 1003.9], [19.9, 82.47, 1015.9], [20.3, 66.88, 1014.8]]

print("\n🚀 Running Optimized MicroPython MLP Model for Weather Prediction...\n")

# ✅ Forward Propagation with More Layers
yout1 = dense(Xtest, w1, b1, 'relu')  # First Hidden Layer
print("\n🔹 Layer 1 Output:", yout1)  # Debugging

yout2 = dense(yout1, w2, b2, 'relu')  # Second Hidden Layer
print("\n🔹 Layer 2 Output:", yout2)  # Debugging

ypred = dense(yout2, w3, b3, 'softmax')  # Output Layer
# print("\n🔹 Final Prediction:", ypred)  # Debugging
output = []

for i in range(len(Xtest)):
    output.append(0)

indexed=[x.index(max(x)) for x in ypred]

season_label = ["Winter","Spring","Summer","Fall"]

for i in range(len(indexed)):
    output[i]=season_label[indexed[i]]

print("Final Output = ",output)

print("\n✅ Optimized MicroPython Weather Prediction Model Completed!")
