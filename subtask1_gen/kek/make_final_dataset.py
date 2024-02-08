import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--d1", default="en_subtask1_test_unlabeled.json"
    )
    parser.add_argument(
        "--output", default="gold_test.json"
    )
    args = parser.parse_args()

    with open(args.d1, "r") as f:
        d1 = json.loads(f.read())

    result = []
    for x in d1:
        #x["output"] = eval(x["output"])
        x["id"] = f'{x["id"]}'
        x["input"] = x["text"]
        result.append(x)

    with open(args.output, "w") as f:
        print(json.dumps(result, indent=4), file=f)


if __name__ == "__main__":
    main()