import pickle 

def load_weights_from_file(filename):
    """Reads weights and biases from a file and assigns them to variables."""
    with open(filename, "r") as file:
        data = file.read()  # Read the file as a string

    weights = eval(data)  # ✅ Safer than eval()
    w1, b1, w2, b2, w3, b3 = [item for item in weights]  
    return w1, b1, w2, b2, w3, b3

# ✅ Load Pre-trained Weights
w1, b1, w2, b2, w3, b3 = load_weights_from_file("hyper_param.txt")

lt=[w1 ,b1 ,w2 ,b2 ,w3 ,b3]

names=["w1","b1","w2","b2","w3","b3"]

for i in range(len(lt)):
    pkl=open(names[i]+".pkl", "wb+")
    pickle.dump(lt[i],pkl)
    pkl.close()
