from backend.core.predictor import predict

while True:
    msg = input("You: ")
    print("Intent:", predict(msg))
