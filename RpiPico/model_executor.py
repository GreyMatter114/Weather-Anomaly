import math
import asyncio
from sensor_reader import sensor_data, data_lock

# ✅ Activation Functions
def relu(x):
    return [max(0, i) for i in x]

def softmax(x_batch, T=2):
    """Memory-efficient softmax"""
    result = []
    for row in x_batch:
        max_x = max(row)
        exp_x = [math.exp((i - max_x) / T) for i in row]
        sum_exp_x = sum(exp_x)
        result.append([i / sum_exp_x for i in exp_x])  
    return result

# ✅ Character-by-Character Parsing Function
def parse_weight_file(file_path):
    """Reads and parses weight and bias matrices from the file character by character"""
    weights_biases = []
    buffer = ""
    in_number = False  

    with open(file_path, "r") as file:
        char = file.read(1)  

        while char:
            if char.isdigit() or char in "-.eE":  
                buffer += char
                in_number = True
            elif in_number:  
                try:
                    weights_biases.append(float(buffer))  
                except ValueError:
                    pass
                buffer = ""
                in_number = False

            char = file.read(1)  

        if in_number and buffer:
            try:
                weights_biases.append(float(buffer))
            except ValueError:
                print(f"⚠️ Invalid number at end of file: {buffer}")

    index = 0

    weight1 = [weights_biases[index + i * 64 : index + (i + 1) * 64] for i in range(3)]
    index += 3 * 64
    bias1 = weights_biases[index : index + 64]
    index += 64

    weight2 = [weights_biases[index + i * 64 : index + (i + 1) * 64] for i in range(64)]
    index += 64 * 64
    bias2 = weights_biases[index : index + 64]
    index += 64

    weight3 = [weights_biases[index + i * 4 : index + (i + 1) * 4] for i in range(64)]
    index += 64 * 4
    bias3 = weights_biases[index : index + 4]

    return [(weight1, bias1), (weight2, bias2), (weight3, bias3)]

# ✅ Dense Function
def dense(x_row, weights, biases, activation):
    """Computes dense layer output"""
    output = [sum(x * w for x, w in zip(x_row, col)) + b for col, b in zip(zip(*weights), biases)]
    
    if activation == "relu":
        return relu(output)
    elif activation == "softmax":
        return softmax([output], T=3)[0]
    return output

# ✅ Model Execution Function
async def run_model():
    weight_file = "hyper_param.txt"
    weights_biases = parse_weight_file(weight_file)

    season_label = ["Winter", "Spring", "Summer", "Fall"]

    while True:
        async with data_lock:
            temp = sensor_data["temperature"]
            hum = sensor_data["humidity"]
            pres = sensor_data["pressure"]

        if temp is None or hum is None or pres is None:
            print("⏳ Waiting for valid sensor readings...")
            await asyncio.sleep(1)
            continue

        test_input = [temp, hum, pres]
        print(f"\nProcessing input: {test_input}")

        # ✅ Layer 1
        yout1 = dense(test_input, *weights_biases[0], 'relu')

        # ✅ Layer 2
        yout2 = dense(yout1, *weights_biases[1], 'relu')

        # ✅ Output Layer
        ypred = dense(yout2, *weights_biases[2], 'softmax')

        # ✅ Final Output Processing
        indexed = ypred.index(max(ypred))
        output = season_label[indexed]

        print(f"🌍 Predicted Season: {output}")

        await asyncio.sleep(10)  # Simulate lag due to computation
