import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--d1", default="output.json"
    )
    parser.add_argument(
        "--d2", default="train.json"
    )
    parser.add_argument(
        "--d3", default="validation.json"
    )
    parser.add_argument(
        "--output", default="final_train.json"
    )
    args = parser.parse_args()

    with open(args.d1, "r") as f:
        d1 = json.loads(f.read())
    with open(args.d2, "r") as f:
        d2 = json.loads(f.read())
    with open(args.d3, "r") as f:
        d3 = json.loads(f.read())

    result = []
    for x in d1:
        x["output"] = eval(x["output"])
        x["id"] = f'output_{x["id"]}'
        result.append(x)

    for x in d2:
        x["output"] = x["labels"]
        x["input"] = x["text"]
        x["id"] = f'train_{x["id"]}'
        result.append(x)


    for x in d3:
        x["output"] = x["labels"]
        x["input"] = x["text"]
        x["id"] = f'validation_{x["id"]}'
        result.append(x)


    with open(args.output, "w") as f:
        print(json.dumps(result, indent=4), file=f)


if __name__ == "__main__":
    main()