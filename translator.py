"""
translator.py - translation logic (no Streamlit code here).

Supported directions (pretrained MarianMT / OPUS-MT models from Hugging Face):
    English -> Hindi : Helsinki-NLP/opus-mt-en-hi
    Hindi -> English : Helsinki-NLP/opus-mt-hi-en
"""
import re

import torch
from transformers import MarianMTModel, MarianTokenizer

# Language name shown in the UI -> language code
LANGUAGES = {"English": "en", "Hindi": "hi"}

# (source code, target code) -> Hugging Face model name
MODEL_REGISTRY = {
    ("en", "hi"): "Helsinki-NLP/opus-mt-en-hi",
    ("hi", "en"): "Helsinki-NLP/opus-mt-hi-en",
}

MAX_CHARS = 2000  # keeps CPU memory use reasonable


def detect_script(text):
    """Return 'devanagari', 'latin' or 'unknown' depending on which letters dominate."""
    devanagari = sum(1 for ch in text if "\u0900" <= ch <= "\u097F")
    latin = sum(1 for ch in text if ch.isascii() and ch.isalpha())
    if devanagari == 0 and latin == 0:
        return "unknown"
    return "devanagari" if devanagari >= latin else "latin"


def validate_input(text, source, target):
    """Check the input. Returns the cleaned text or raises ValueError with a friendly message."""
    if (source, target) not in MODEL_REGISTRY:
        raise ValueError("Please select two different languages (English and Hindi).")
    if text is None or not text.strip():
        raise ValueError("Please enter some text to translate.")
    text = re.sub(r"\s+", " ", text).strip()  # collapse extra spaces / line breaks
    if len(text) > MAX_CHARS:
        raise ValueError(f"Text is too long ({len(text)} characters). Limit is {MAX_CHARS}.")
    script = detect_script(text)
    if script == "unknown":
        raise ValueError("The text has no letters to translate.")
    if source == "en" and script == "devanagari":
        raise ValueError("The text looks like Hindi, but the source language is English.")
    if source == "hi" and script == "latin":
        raise ValueError("The text looks like English, but the source language is Hindi.")
    return text


def load_model(source, target):
    """Download (first time only) and load the tokenizer and model for a language pair."""
    name = MODEL_REGISTRY[(source, target)]
    tokenizer = MarianTokenizer.from_pretrained(name)
    model = MarianMTModel.from_pretrained(name)
    model.eval()  # inference mode (dropout off)
    return tokenizer, model


def split_sentences(text):
    """Split after . ! ? and the Hindi danda so each sentence is translated separately."""
    parts = re.split(r"(?<=[.!?\u0964])\s+", text)
    return [p for p in parts if p.strip()]


def translate(text, tokenizer, model):
    """Translate already-validated text using a loaded tokenizer and model."""
    sentences = split_sentences(text)
    batch = tokenizer(sentences, return_tensors="pt", padding=True,
                      truncation=True, max_length=512)
    with torch.no_grad():  # no gradients needed for inference
        generated = model.generate(**batch, num_beams=4, max_new_tokens=256)
    outputs = tokenizer.batch_decode(generated, skip_special_tokens=True)
    return " ".join(o.strip() for o in outputs).strip()
