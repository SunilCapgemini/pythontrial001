from transformers import AutoModelForCausalLM, AutoTokenizer

# Path to your local model directory
model_path = "./output/checkpoint-30"

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
print(f'\n\n{tokenizer}\n\n')
# messages = [
#     {
#         "role": "system",
#         "content": "You are a friendly chatbot who always responds in the style of pirate"
#     },
#     {
#         'role': 'user',
#         'content': "How man helicopters can a human eat in one sitting?"
#     }
# ]

# template = [
#     {"role": "system", "content": "{system_message}"},
#     {"role": "user", "content": "{user_message}"}
# ]
# tokenized_chat = tokenizer.apply_chat_template(messages,template=template,tokenize=True, add_generation_prompt=True, return_tensors="pt")
# print(tokenized_chat)
# # Encode input text
input_text = "### Question:\nwrite a react js code \n### Answer:\n"
input_ids = tokenizer.encode(input_text, return_tensors='pt')

# Generate text
output = model.generate(input_ids, max_length=5000, 
                        num_return_sequences=1,
                        num_beams=10,
                        do_sample=True,
                        # top_k=50,
                        top_p=0.92,
                        temperature=0.7,
                        no_repeat_ngram_size=2,
                        early_stopping=True,
                        )

# Decode the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)