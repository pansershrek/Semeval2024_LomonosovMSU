import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source_file", default="llama_2_result_semeval.json"
    )
    parser.add_argument(
        "--result_file", default="to_submit_llama_2_result_semeval.json"
    )
    args = parser.parse_args()

    with open(args.source_file, "r") as f:
        data = json.loads(f.read())

    result = []
    exceptions = 0
    for x in data:
        tmp = {
            "id": int(x["id"]),
            "generated_text": []
        }
        try:
            generated_text = x["generated_text"]
            if "Output:" in generated_text:
                generated_text = generated_text[
                    x["generated_text"].find("Output:")+len("Output:")
                    :
                ].strip()
            #print(generated_text)
            #generated_text = generated_text.split("Output:")[].strip()
            generated_text = generated_text.split("]")[0] + "]"
            generated_text = generated_text.replace(
                "'Misrepresentation of Someone's Position'",
                '"Misrepresentation of Someone'+"'"+'s Position (Straw Man)"'
            )
            generated_text = generated_text.replace(
                "'Misrepresentation of Someone's Position (Straw Man)'",
                '"Misrepresentation of Someone'+"'"+'s Position (Straw Man)"'
            )
            generated_text = generated_text.replace("'Smears" +'"', "'Smears'")
            generated_text = eval(generated_text)
            tmp["generated_text"] = generated_text
        except Exception as e:
            exceptions += 1
            print(tmp["id"])
            #print(e, tmp["id"])
            #print(generated_text)
            #exit(0)
        result.append(tmp)
    print("Exceptions", exceptions)

    with open(args.result_file, "w") as f:
        print(json.dumps(result, indent=4), file=f)



if __name__ == "__main__":
    main()