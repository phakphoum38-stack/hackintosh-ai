from backend.core.db_dataset import fetch_logs

def build_dataset_from_db():

    logs = fetch_logs()

    dataset = []

    for cpu, gpu, success in logs:

        dataset.append({
            "x": [50, 50, 50],  # placeholder feature vector
            "y": success
        })

    return dataset


def update_learning_pipeline():

    data = build_dataset_from_db()

    print(f"Loaded dataset size: {len(data)}")

    return data
