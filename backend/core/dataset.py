def load_dataset():
    path = "YOUR_PATH_HERE.json"

    print("Loading dataset from:", path)

    with open(path, "r") as f:
        content = f.read()
        print("RAW DATA:", repr(content[:200]))

        data = json.loads(content)

    return data
