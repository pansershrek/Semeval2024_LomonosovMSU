import json
import argparse
import random


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset", default="final_gold.json"
    )
    parser.add_argument(
        "--output", default="final_gold_fixed.json"
    )
    args = parser.parse_args()

    result = []

    with open(args.dataset, "r") as f:
        dataset = json.loads(f.read())

    ln = 0

    for x in dataset:
        x["input"] = x["input"].replace("\\n", "^")
        x["input"] = x["input"].replace('\\', "")
        x["input"] = x["input"].replace("^", "\n")
        x["input"] = x["input"].strip()
        #if "Input:" not in x["input"]:
        #    x["input"] = (
        #        "Your goal is to identify rhetorical and psychological techniques in the given text.\n"+
        #        "Input:"+
        #        x["input"]
        #    )
        if "Input:" in x["input"]:
            l = len("Your goal is to identify rhetorical and psychological techniques in the given text.\n")
            x["input"] = x["input"][l:]
        else:
            x["input"] = "Input:"+x["input"]
        x["input"] = "Your goal is to identify rhetorical and psychological techniques in the given text.\n" + x["input"]
        if "Output:" not in x["input"]:
            x["input"] = x["input"]+"\nOutput:"
        #if "Output:" in x["input"]:
        #    full_input = f'{x["input"]}{json.dumps(x["output"])}'
        #else:
        #    full_input = f'{x["input"]}\nOutput:{json.dumps(x["output"])}'
        tmp = {
            "id": x["id"],
            "input": x["input"],
            "output": x["output"],
            "full_input": f'{x["input"]}{json.dumps(x["output"])}'
        }
        if len(tmp["full_input"]) > 4096:
            continue
        ln = max(ln, len(tmp["full_input"]))
        result.append(tmp)

    random.shuffle(result)

    with open(args.output, "w") as f:
        print(json.dumps(result, indent=4), file=f)

    print("Max len", ln)
    print("Dataset len", len(result))

if __name__ == "__main__":
    main()