import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source_file", default="llam2_full_to_submit.json"
    )
    parser.add_argument(
        "--result_file", default="llam2_full_to_submit.txt"
    )
    args = parser.parse_args()

    with open(args.source_file, "r") as f:
        data = json.loads(f.read())

    result = []
    exceptions = 0
    for x in data:
        tmp = {
            "id": x["id"].replace("test_", ""),
            "labels": []
        }
        #print(tmp)
        try:
            generated_text_s = x["generated_text"].strip()
            generated_text_s = generated_text_s.replace("-", "")
            #print(generated_text)
            #print(generated_text.startswith("[]"))
            if generated_text_s.startswith("[]"):
                generated_text = []
            else:
                pref = 0
                # for idx, x in enumerate(generated_text_s):
                #     if x == "[" or (
                #         generated_text_s[idx] == "O" and
                #         generated_text_s[idx] == "u" and
                #         generated_text_s[idx] == "t" and
                #         generated_text_s[idx] == "p" and
                #         generated_text_s[idx] == "u" and
                #         generated_text_s[idx] == "t"
                #     ):
                #         break
                #     else:
                #         pref += 1
                # generated_text = generated_text_s[pref:]
                generated_text = generated_text_s
                if generated_text.startswith("[]"):
                    generated_text = []
                else:
                    generated_text = generated_text.split("\n")[0]
                    generated_text = generated_text.replace("Output:", "")
                    generated_text = eval(generated_text)
            tmp["labels"] = generated_text
        except Exception as e:
            exceptions += 1
            print(tmp["id"], e)
            #print(generated_text)
        result.append(tmp)
        #if exceptions == 1:
        #    break
    print("Exceptions", exceptions)

    with open(args.result_file, "w") as f:
        print(json.dumps(result, indent=4), file=f)



if __name__ == "__main__":
    main()