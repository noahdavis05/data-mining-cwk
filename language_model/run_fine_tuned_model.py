from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


model_name = "star_wars_lora"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

tokenizer.pad_token = tokenizer.eos_token


input_text = "Instruction: Who did Luke Skywalker grow up with?\n\nResponse: "


inputs = tokenizer(input_text, return_tensors="pt").to(device)

# Generate text
output = model.generate(
    **inputs,
    max_length=2000,            
    temperature=0.5,           
    top_p=0.9,                 
    repetition_penalty=1.2,   
    do_sample=True             
)


print(tokenizer.decode(output[0], skip_special_tokens=True))
