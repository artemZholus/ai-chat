from fastapi import FastAPI
from pydantic import BaseModel
from threading import RLock
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from generate_transformers import main


class GPT3Inferencer:
    def __init__(self, device='cuda'):
        self.model_name = 'sberbank-ai/rugpt3medium_based_on_gpt2'
        self.model_type = 'gpt2'
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.model.to(device)

    def generate(self, prompt, k=5, p=0.95, temperature=1., length=30):
        return main(
            prompt=prompt,
            model=self.model,
            tokenizer=self.tokenizer,
            model_type=self.model_type,
            model_name_or_path=self.model_name,
            k=k, p=p, length=length,
            temperature=temperature,
        )

app = FastAPI()
lock = RLock()
gpt3 = GPT3Inferencer(device='cuda')


class Prompt(BaseModel):
    text: str
    k: int = 5
    p: float = 0.95
    temp: float = 1.
    length: int = 30

@app.post('/generate/')
def generate(prompt: Prompt):
    with lock:
        return {
            'reply': gpt3.generate(
                prompt.text,
                k=prompt.k, p=prompt.p,
                temperature=prompt.temp,
                length=prompt.length
            )
        }


