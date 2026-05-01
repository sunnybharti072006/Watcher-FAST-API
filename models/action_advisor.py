from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

print("Loading Flan-T5 model...")
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

# GPU pe move karo
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
print(f"Flan-T5 ready on {device}!")

def get_action(summary: str, url: str) -> str:
    prompt = (
        f"A website at {url} changed. "
        f"Summary: {summary}. "
        f"What specific action should the user take now?"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=512,
        truncation=True
    ).to(device)

    outputs = model.generate(
        **inputs,
        max_length=150,
        num_beams=4,
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)