from transformers import BartForConditionalGeneration, BartTokenizer
import torch

print("Loading BART summarizer...")

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained(
    "facebook/bart-large-cnn"
).to(device)

print("BART ready!")

def summarize(added: str, removed: str, url: str) -> str:
    change_text = f"Website {url} changed."
    if added:
        change_text += f" Added: {added[:400]}."
    if removed:
        change_text += f" Removed: {removed[:400]}."

    if len(change_text) < 60:
        return change_text

    try:
        inputs = tokenizer(
            change_text[:1024],
            return_tensors="pt",
            truncation=True
        ).to(device)

        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=120,
            min_length=20,
            num_beams=4,
            early_stopping=True
        )

        return tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True
        )
    except Exception as e:
        return change_text