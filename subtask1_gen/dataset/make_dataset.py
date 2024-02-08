import argparse
import json
import random

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
    parser.add_argument('--source_data', default="validation.json")
    parser.add_argument('--train', default="instruct_validation_1.json")
    #parser.add_argument('--test', default="instruct_test_1.json")
    args = parser.parse_args()

    with open(args.source_data, "r") as f:
        data = json.loads(f.read())

    random.shuffle(data)

    train = data
    #test = []

    train = convert_to_instract(train)
    #test = convert_to_instract(test)

    with open(args.train, "w") as f:
        print(json.dumps(train, indent=4), file=f)

   # with open(args.test, "w") as f:
    #    print(json.dumps(test, indent=4), file=f)


if __name__ == "__main__":
    main()