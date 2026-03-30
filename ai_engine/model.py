import pandas as pd
import torch
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    TrainingArguments,
    Trainer
)

# -----------------------------
# DOWNLOAD NLTK CORPUS
# -----------------------------

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

nltk.data.path.append("C:/nltk_data")

# -----------------------------
# DEVICE
# -----------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# -----------------------------
# LOAD DATASET
# -----------------------------

df = pd.read_csv("C:\\nextgen_proj\\ai_engine\\clean_task_dataset_50000.csv")

print("Dataset size:", len(df))

# -----------------------------
# NLTK TEXT CLEANING
# -----------------------------

def clean_text(text):

    tokens = word_tokenize(str(text).lower())

    cleaned_tokens = []

    for word in tokens:

        # remove punctuation-like tokens
        if word.isalpha():

            # normalize word using wordnet lemma
            lemma = wordnet.morphy(word)

            if lemma:
                cleaned_tokens.append(lemma)
            else:
                cleaned_tokens.append(word)

    return " ".join(cleaned_tokens)


df["input"] = df["input"].apply(clean_text)
df["output"] = df["output"].apply(clean_text)

# -----------------------------
# CONVERT TO DATASET
# -----------------------------

dataset = Dataset.from_pandas(df)

# -----------------------------
# TOKENIZER
# -----------------------------

tokenizer = AutoTokenizer.from_pretrained("t5-small")

# -----------------------------
# PREPROCESS FUNCTION
# -----------------------------

def preprocess(example):

    inputs = tokenizer(
        example["input"],
        padding="max_length",
        truncation=True,
        max_length=64
    )

    targets = tokenizer(
        example["output"],
        padding="max_length",
        truncation=True,
        max_length=128
    )

    labels = targets["input_ids"]

    labels = [
        token if token != tokenizer.pad_token_id else -100
        for token in labels
    ]

    inputs["labels"] = labels

    return inputs


dataset = dataset.map(preprocess)

dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)

# -----------------------------
# MODEL
# -----------------------------

model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

model = model.to(device)

# -----------------------------
# TRAINING CONFIG
# -----------------------------

training_args = TrainingArguments(
    output_dir="./task_generator_model",
    num_train_epochs=5,
    per_device_train_batch_size=4,
    learning_rate=3e-4,
    save_steps=500,
    logging_steps=50,
    fp16=True
)

# -----------------------------
# TRAINER
# -----------------------------

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()

# -----------------------------
# SAVE MODEL
# -----------------------------

trainer.save_model("./task_generator_model")
tokenizer.save_pretrained("./task_generator_model")

print("Model saved!")

# -----------------------------
# TEST GENERATION
# -----------------------------

def generate_task(prompt):

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    outputs = model.generate(
        **inputs,
        max_length=120,
        num_beams=4
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return result


print("\nExample generation:")
print(generate_task("speech recognition"))