import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# -----------------------------
# DEVICE
# -----------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# -----------------------------
# LOAD MODEL
# -----------------------------

MODEL_PATH = "./task_generator_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

model = model.to(device)
model.eval()

print("Model loaded successfully")

# -----------------------------
# GENERATE RANDOM TASK
# -----------------------------

def generate_task(topic):

    inputs = tokenizer(
        topic,
        return_tensors="pt"
    ).to(device)

    outputs = model.generate(
        **inputs,

        max_length=120,

        do_sample=True,          # enables randomness
        temperature=0.9,         # creativity
        top_k=50,                # token pool
        top_p=0.95,              # nucleus sampling

        repetition_penalty=1.2
    )

    result = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return result


# -----------------------------
# TEST MULTIPLE RANDOM TASKS
# -----------------------------

topic = "Speech Recognition"

print("\nGenerating multiple tasks for:", topic)

for i in range(5):

    print("\nTask", i+1)
    print(generate_task(topic))


# -----------------------------
# INTERACTIVE MODE
# -----------------------------

print("\n--- Interactive Mode ---")

while True:

    topic = input("\nEnter topic (or exit): ")

    if topic.lower() == "exit":
        break

    print("\nGenerated Task:\n")
    print(generate_task(topic))