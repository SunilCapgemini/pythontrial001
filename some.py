from datasets import load_dataset
from transformers import AutoModelForCausalLM,AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('HuggingFaceTB/SmolLM2-1.7B')
data = load_dataset('wikitext', 'wikitext-2-raw-v1')
data['train'] = data['train'].select(range(10))
print(data['train']['text'])
# data = data.map(lambda x: tokenizer(x['text'], truncation=True, max_length=50),remove_columns=['text'])
# print(data['train'].to_pandas())

