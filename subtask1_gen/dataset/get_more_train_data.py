import argparse
import json
import random
import os

propaganda_types = [
    'Doubt', 'Causal Oversimplification',
    'Flag-waving', 'Appeal to fear/prejudice',
    'Loaded Language', 'Obfuscation, Intentional vagueness, Confusion',
    'Smears', 'Name calling/Labeling', 'Thought-terminating cliché',
    'Slogans', 'Presenting Irrelevant Data (Red Herring)',
    'Glittering generalities (Virtue)', 'Black-and-white Fallacy/Dictatorship',
    'Bandwagon', 'Exaggeration/Minimisation', 'Reductio ad hitlerum',
    "Misrepresentation of Someone's Position (Straw Man)", 'Whataboutism',
    'Appeal to authority', 'Repetition'
]

t2t = {
    "Appeal_to_Authority": 'Appeal to authority',
    "Appeal_to_Popularity": None,
    "Appeal_to_Values": None,
    "Appeal_to_Fear-Prejudice": 'Appeal to fear/prejudice',
    "Flag_Waving": 'Flag-waving',
    "Causal_Oversimplification": 'Causal Oversimplification',
    "False_Dilemma-No_Choice": None,
    "Consequential_Oversimplification": None,
    "Straw_Man": "Misrepresentation of Someone's Position (Straw Man)",
    "Red_Herring": 'Presenting Irrelevant Data (Red Herring)',
    "Whataboutism": 'Whataboutism',
    "Slogans": "Slogans",
    "Appeal_to_Time": None,
    "Conversation_Killer": None,
    "Loaded_Language": 'Loaded Language',
    "Repetition": "Repetition",
    "Exaggeration-Minimisation": 'Exaggeration/Minimisation',
    "Obfuscation-Vagueness-Confusion": 'Obfuscation, Intentional vagueness, Confusion',
    "Name_Calling-Labeling": 'Name calling/Labeling',
    "Doubt": 'Doubt',
    "Guilt_by_Association": None,
    "Appeal_to_Hypocrisy": None,
    "Questioning_the_Reputation": None,
}


INSTRUCTION = "Your goal is to identify rhetorical and psychological techniques in the given text."

def convert_to_instract(dataset):
    result = []
    for x in dataset:
        result.append(
            {
                "id": x["id"],
                "input": f"{INSTRUCTION}\nInput:{x['text']}\nOutput:",
                "full_input": f"{INSTRUCTION}\nInput:{x['text']}\nOutput:{x['labels']}",
                "output": f"{x['labels']}"
            }
        )
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', default="/Users/g.skiba/Downloads/semeval2023task3bundle-v4/data/en/train-labels-subtask-3")
    parser.add_argument('--output', default="output.json")
    args = parser.parse_args()

    data = []
    for x in os.listdir(args.folder):
        print(x)
        if x.endswith(".txt"):
            a = []
            b = []
            with open(os.path.join(args.folder, x), "r") as f:
                for line in f:
                    a.append(line)
            with open(os.path.join(args.folder, f"{x}.template"), "r") as f:
                for line in f:
                    b.append(line)
            for xx, yy in zip(a, b):
                xxx = xx.strip().split("\t")
                yyy = yy.strip().split("\t")
                if len(xxx) == 2:
                    data.append({
                        "id": f"{xxx[0]}_{xxx[1]}",
                        "text": yyy[-1],
                        "labels": []
                    })
                else:
                    t = xxx[2].split(",")
                    t = [t2t[w] for w in t if t2t[w] is not None]
                    data.append({
                        "id": f"{xxx[0]}_{xxx[1]}",
                        "text": yyy[-1],
                        "labels": t,
                    })
    with open(args.output, "w") as f:
        print(json.dumps(convert_to_instract(data), indent=4), file=f)

if __name__ == "__main__":
    main()