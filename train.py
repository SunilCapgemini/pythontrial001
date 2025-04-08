# Code adapted from https://github.com/huggingface/trl/blob/main/examples/research_projects/stack_llama/scripts/supervised_finetuning.py
# and https://huggingface.co/blog/gemma-peft
import argparse
import multiprocessing
import os

import torch
import transformers
# from accelerate import PartialState
from datasets import load_dataset
from peft import AutoPeftModelForCausalLM, LoraConfig
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    is_torch_npu_available,
    is_torch_xpu_available,
    logging,
    set_seed,
)
from trl import SFTConfig, SFTTrainer


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_id", type=str, default="HuggingFaceTB/SmolLM2-1.7B")
    parser.add_argument("--tokenizer_id", type=str, default="")
    parser.add_argument("--dataset_name", type=str, default="bigcode/the-stack-smol")
    parser.add_argument("--subset", type=str, default="data/python")
    parser.add_argument("--split", type=str, default="train")
    parser.add_argument("--streaming", type=bool, default=False)
    parser.add_argument("--dataset_text_field", type=str, default="content")

    parser.add_argument("--max_seq_length", type=int, default=2048)
    parser.add_argument("--max_steps", type=int, default=1000)
    parser.add_argument("--micro_batch_size", type=int, default=1)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=4)
    parser.add_argument("--weight_decay", type=float, default=0.01)
    parser.add_argument("--bf16", type=bool, default=True)

    parser.add_argument("--use_bnb", type=bool, default=False)
    parser.add_argument("--attention_dropout", type=float, default=0.1)
    parser.add_argument("--learning_rate", type=float, default=2e-4)
    parser.add_argument("--lr_scheduler_type", type=str, default="cosine")
    parser.add_argument("--warmup_steps", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output_dir", type=str, default="finetune_smollm2_python")
    parser.add_argument("--num_proc", type=int, default=None)
    parser.add_argument("--push_to_hub", type=bool, default=True)
    parser.add_argument("--repo_id", type=str, default="SmolLM2-1.7B-finetune")
    return parser.parse_args()


def main(args):
    # config
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"],
        bias="none",
        task_type="CAUSAL_LM",
    )
    bnb_config = None
    if args.use_bnb:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

    
    tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M",quantization_config=bnb_config,attention_dropout=0.1,)
    # model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M")
    model = AutoModelForCausalLM.from_pretrained("output/checkpoint-30")



    data = load_dataset('wikitext', 'wikitext-2-raw-v1')


    data['train'] = data['train'].select(range(10))

    def tokenize_function(examples):
        return tokenizer(examples["text"])
    
    
    tokenized_datasets = data.map(tokenize_function, batched=True, num_proc=1, remove_columns=["text"])
    
    def group_texts(examples):
        # Concatenate all texts.
        block_size = 128
        concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
            # customize this part to your needs.
        total_length = (total_length // block_size) * block_size
        # Split by chunks of max_len.
        result = {
            k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
            for k, t in concatenated_examples.items()
        }
        result["labels"] = result["input_ids"].copy()
        return result


    lm_datasets = tokenized_datasets.map(
        group_texts,
        batched=True,
        batch_size=1000,
        num_proc=8,
    )


    # setup the trainer
    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=lm_datasets['train'],
        args=SFTConfig(
            dataset_num_proc=1,
            max_seq_length=50,
            per_device_train_batch_size=2,
            learning_rate=4e-5,
            weight_decay=0.1,
            num_train_epochs=100,
            bf16=True,
            output_dir='output',
        ),
        peft_config=lora_config,
    )

    # launch
    print("Training...")
    trainer.train()
    print("Training Done! 💥")


if __name__ == "__main__":
    args = get_args()
    set_seed(args.seed)
    os.makedirs(args.output_dir, exist_ok=True)

    logging.set_verbosity_error()

    main(args)