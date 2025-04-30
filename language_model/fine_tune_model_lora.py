from transformers import Trainer, TrainingArguments, AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from peft import get_peft_model, LoraConfig, TaskType
import torch

# Load dataset
dataset = load_dataset('json', data_files={'train': 'processed_data/question_and_answers.jsonl'})
train_dataset = dataset['train']

# Load tokenizer and model
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # Ensure padding token is set

base_model = AutoModelForCausalLM.from_pretrained(model_name)

# Define LoRA config
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],  # adjust depending on architecture
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Wrap model with PEFT
model = get_peft_model(base_model, lora_config)

# Move to CPU
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

# Preprocess dataset
train_dataset = train_dataset.map(preprocess_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results_lora",
    evaluation_strategy="no",
    logging_dir="./logs_lora",
    logging_steps=200,
    save_steps=1000,
    save_total_limit=2,
    learning_rate=5e-5,
    per_device_train_batch_size=1,
    num_train_epochs=3,
    weight_decay=0.01,
    gradient_accumulation_steps=8,
    dataloader_num_workers=0,
    no_cuda=True,
    report_to=None
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

# Train the model
trainer.train()

# Save the LoRA-adapted model
model.save_pretrained("star_wars_lora")
tokenizer.save_pretrained("star_wars_lora")
