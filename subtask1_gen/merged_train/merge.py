import json
import argparse
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--d1", default="final_gold_fixed.json"
    )
    parser.add_argument(
        "--d2", default="final_train_fixed.json"
    )
    parser.add_argument(
        "--output", default="full_dataset_to_train.json"
    )
    args = parser.parse_args()

    with open(args.d1, "r") as f:
        d1 = json.loads(f.read())
    with open(args.d2, "r") as f:
        d2 = json.loads(f.read())

    result = []

    for x in d1:
        result.append(x)

    for x in d2:
        result.append(x)

    random.shuffle(result)

    with open(args.output, "w") as f:
        print(json.dumps(result, indent=4), file=f)


if __name__ == "__main__":
    main()