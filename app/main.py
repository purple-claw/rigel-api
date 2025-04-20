from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from app.loadModel import get_model

app = FastAPI()

class ClauseInput(BaseModel):
    text: str

@app.post("/")
async def analyze(input: ClauseInput):
    model, tokenizer = get_model()

    inputs = tokenizer(input.text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.nn.functional.softmax(logits, dim=1)
        label = torch.argmax(probs).item()

    return {
        "label": "RISKY" if label == 1 else "SAFE",
        "confidence": round(probs[0][label].item(), 4),
        "probabilities": {
            "SAFE (0)": round(probs[0][0].item(), 4),
            "RISKY (1)": round(probs[0][1].item(), 4)
        }
    }
