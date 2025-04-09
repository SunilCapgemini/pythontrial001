# import torch

# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
# from datasets import Dataset,DatasetDict
# from peft import LoraConfig
# from trl import SFTTrainer,SFTConfig

def callmain():
    text = ''
    with open('trial001/data001.txt') as file:
        lines = file.readlines()
        print(lines)


callmain()