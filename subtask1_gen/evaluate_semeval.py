import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--predict", default="result_mistral.json"
    )
    parser.add_argument(
        "--val_dataset", default="dataset/instruct_validation_1.json"
    )
    args = parser.parse_args()

    with open(args.predict, "r") as f:
        predict = json.loads(f.read())

    with open(args.val_dataset, "r") as f:
        val_dataset = json.loads(f.read())

    acc = 0.0

    for x, y in zip(predict, val_dataset):
        pred_result = x["generated_text"]
        val_result = y["output"]
        val_result = eval(val_result)
        if pred_result == val_result:
            acc += 1

    print(f"Accurasy {acc / len(predict) * 100}")



if __name__ == "__main__":
    main()