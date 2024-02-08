import argparse
import json
from sklearn.metrics import f1_score

entities = ['O', 'PER', 'ORG', 'LOC', 'MISC']

entities2id = {y: x for x, y in enumerate(entities)}
id2entities = {x: y for x, y in enumerate(entities)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default="llama2_generated_output.json")
    args = parser.parse_args()

    with open(args.filename, "r") as f:
        data = json.loads(f.read())

    ans = {
        "correct": [],
        "predict": [],
    }

    preds = {}
    for x in data:
        pred_id = int(x["full_id"].split("_")[0])
        if pred_id not in preds:
            preds[pred_id] = []
        preds[pred_id].append(x)

    agg_pred = {}
    hallucination = 0
    for k, v in preds.items():
        converted_ner_tags = v[0]["converted_ner_tags"]
        generated_text = {
            x["entity"]: x["generated_text"].split(
                "Output:"
            )[0].split("\n")[0].strip()
            for x in v
        }
        pred = [0 for x in converted_ner_tags]
        converted_ner_tags = [entities2id[x] for x in converted_ner_tags]
        #print(len(converted_ner_tags))
        #print(len(generated_text["PER"].split(" ")))
        flag = False
        for k1, v1 in generated_text.items():
            for a, b in enumerate(v1.split(" ")):
                if "@@" in b and "##" in b:
                    try:
                        pred[a] = entities2id[k1]
                    except:
                        flag = True
                        hallucination += 1
                        #print(v[0]["converted_ner_tags"])
                        #print(v[0]["generated_text"])
                        #print(v1)
                        #raise
                if flag:
                    break
            if flag:
                break
        if flag:
            pred = [0 for x in converted_ner_tags]
        ans["correct"].append(converted_ner_tags)
        ans["predict"].append(pred)

    correct = []
    predict = []
    for x in ans["correct"]:
        correct += x
    for x in ans["predict"]:
        predict += x

    f1_macro = f1_score(correct, predict, average = "macro")
    f1_micro = f1_score(correct, predict, average = "micro")

    print(f"F1 macro: {f1_macro}")
    print(f"F1 micro: {f1_micro}")
    print(f"Hallucination: {hallucination}")

    f1_macro_avg = 0
    f1_micro_avg = 0
    for x, y in zip(ans["correct"], ans["predict"]):
        f1_macro_avg += f1_score(x, y, average='macro')
        f1_micro_avg += f1_score(x, y, average='micro')

    print(f"F1 macro avg: {f1_macro_avg / len(ans['predict'])}")
    print(f"F1 micro avg: {f1_micro_avg / len(ans['predict'])}")


if __name__ == "__main__":
    main()