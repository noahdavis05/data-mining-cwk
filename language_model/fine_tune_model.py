# This file uses full fine tuning fot the tinyllama model
from transformers import Trainer, TrainingArguments, AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import torch

# Load dataset
dataset = load_dataset('json', data_files={'train': '../training_data/processed_data/question_and_answers_2.jsonl'})
train_dataset = dataset['train']

# Load pre-trained model and tokenizer
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" 
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token  

# Ensure model runs on CPU
device = torch.device("cpu")
model.to(device)

# Tokenization function
def preprocess_function(examples):
    encoding = tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=512
    )
    encoding["labels"] = encoding["input_ids"].copy()
    return encoding

# Apply preprocessing
train_dataset = train_dataset.map(preprocess_function, batched=True)

# Training arguments (optimized for CPU)
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="no",
    logging_dir="./logs",
    logging_steps=200,
    save_steps=1000,
    save_total_limit=2,
    learning_rate=5e-5,
    per_device_train_batch_size=1, 
    per_device_eval_batch_size=1,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=False,
    gradient_accumulation_steps=8,
    dataloader_num_workers=0,
    no_cuda=True, 
    report_to=None  
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

# Start training
trainer.train()

# Save model and tokenizer
model.save_pretrained("star_wars_3")
tokenizer.save_pretrained("star_wars_3")
