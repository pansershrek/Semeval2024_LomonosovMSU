import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--d1", default="dev_subtask1_en.json"
    )
    parser.add_argument(
        "--output", default="final_gold.json"
    )
    args = parser.parse_args()

    with open(args.d1, "r") as f:
        d1 = json.loads(f.read())

    result = []
    for x in d1:
        x["output"] = x["labels"]
        x["input"] = x["text"]
        x["id"] = f'gold_{x["id"]}'
        result.append(x)


    with open(args.output, "w") as f:
        print(json.dumps(result, indent=4), file=f)


if __name__ == "__main__":
    main()