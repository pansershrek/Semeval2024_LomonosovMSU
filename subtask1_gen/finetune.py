import argparse
import json

from datasets import load_dataset
import torch
import wandb
from peft import (
    LoraConfig,
    get_peft_model,
    get_peft_model_state_dict,
    prepare_model_for_kbit_training
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments
)

from utils import set_random_seed, fix_tokenizer, fix_model

def prepare_llama_pro(model):
    for x, y in model.named_parameters():
        if "model.layers" in x:
            num = int(x.split(".")[2])
            if (num + 1) % 4 != 0:
                y.requires_grad = True
        y.requires_grad = True
    return model

def get_dataset(data_path, tokenizer, max_length):
    def tokenize(tmp):
        input_ids = tokenizer(
            tmp["full_input"],
            truncation = True,
            max_length = max_length,
            padding = "max_length"
        )["input_ids"]
        input_ids_not_mask = tokenizer(
            tmp["output"],
            truncation = True,
            max_length = max_length
        )["input_ids"]
        mask_len = (
            len(input_ids) - len(input_ids_not_mask)
        )
        return {
            "input_ids": input_ids,
            "labels": (
                [-100] * mask_len + input_ids[mask_len:]
            ),
            "attention_mask": [1] * len(input_ids),
        }
    dataset = load_dataset("json", data_files=data_path)["train"]
    return dataset.map(tokenize)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", default="/data/semeval2024/llama_pro.json"
    )
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.loads(f.read())

    set_random_seed(config["SEED"])

    tokenizer = AutoTokenizer.from_pretrained(config["MODEL_NAME"])
    #tokenizer.pad_token = tokenizer.unk_token
    tokenizer = fix_tokenizer(tokenizer)

    model = AutoModelForCausalLM.from_pretrained(
        config["MODEL_NAME"],
        device_map = config["TRAIN_PARAMS"]["DEVICE_MAP"],
        torch_dtype=torch.float16,
        #load_in_8bit = config["TRAIN_PARAMS"]["LOAD_IN_8BIT"],
        use_flash_attention_2 = config["TRAIN_PARAMS"]["USE_FLASH_ATTENTION_2"]
    )
    fix_model(model, tokenizer, use_resize=False)
    if config["MODEL_NAME"] == "TencentARC/LLaMA-Pro-8B":
        model = prepare_llama_pro(model)
    #model = prepare_model_for_kbit_training(model)
    #model.config.pad_token_id = tokenizer.pad_token_id
    #model.config.max_length = config["TRAIN_PARAMS"]["MAX_LEN"]
    lora_config = LoraConfig(
        r = config["LORA_PARAMS"]["LORA_R"],
        lora_alpha = config["LORA_PARAMS"]["LORA_ALPHA"],
        target_modules = config["LORA_PARAMS"]["TARGET_MODULES"],
        lora_dropout = config["LORA_PARAMS"]["LORA_DROPOUT"],
        bias = "none",
        task_type = "CAUSAL_LM",
    )
    #model = get_peft_model(model, lora_config)

    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    train_dataset = get_dataset(
        config["TRAIN_DATASET"], tokenizer, config["TRAIN_PARAMS"]["MAX_LEN"]
    )
    test_dataset = get_dataset(
        config["TEST_DATASET"], tokenizer, config["TRAIN_PARAMS"]["MAX_LEN"]
    )

    trainer = Trainer(
        model = model,
        train_dataset = train_dataset,
        #eval_dataset = test_dataset,
        args = TrainingArguments(
            report_to = config["TRAIN_PARAMS"]["REPORT_TO"],
            per_device_train_batch_size = (
                config["TRAIN_PARAMS"]["MICRO_BATCH_SIZE"]
            ),
            gradient_accumulation_steps = (
                config["TRAIN_PARAMS"]["GRADIENT_ACCUMULATION_STEPS"]
            ),
            warmup_steps = config["TRAIN_PARAMS"]["WARMUP_STEPS"],
            num_train_epochs = config["TRAIN_PARAMS"]["EPOCHS"],
            learning_rate = config["TRAIN_PARAMS"]["LEARNING_RATE"],
            fp16 = config["TRAIN_PARAMS"]["FP16"],
            logging_steps = 1,
            evaluation_strategy="no",
            output_dir = config["MODEL_OUTPUT"],
            save_safetensors = False
        ),
        data_collator=data_collator,
    )

    #model.config.use_cache = False

    #old_state_dict = model.state_dict
    #model.state_dict = (
    #    lambda self, *_, **__: get_peft_model_state_dict(self, old_state_dict())
    #).__get__(model, type(model))

    #if torch.__version__ >= "2":
    #    model = torch.compile(model)

    with wandb.init(project="semeval2024_Task1") as run:
        #model.print_trainable_parameters()
        #trainer.train(resume_from_checkpoint=True)
        trainer.train()

    model.save_pretrained(config["MODEL_OUTPUT"], safe_serialization=False)



if __name__ == "__main__":
    main()
