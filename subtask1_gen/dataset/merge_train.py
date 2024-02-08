import argparse
import json
import random


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default="instruct_train_1.json")
    parser.add_argument('--output', default="output.json")
    parser.add_argument('--new_train', default="new_instruct_train_1.json")
    args = parser.parse_args()

    with open(args.train, "r") as f:
        train = json.loads(f.read())

    with open(args.output, "r") as f:
        output = json.loads(f.read())

    new_train = train + output

    random.shuffle(new_train)

    with open(args.new_train, "w") as f:
        print(json.dumps(new_train, indent=4), file=f)


if __name__ == "__main__":
    main()