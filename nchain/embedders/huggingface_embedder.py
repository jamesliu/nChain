from transformers import AutoTokenizer, AutoModel
from .base_embedder import BaseEmbedder
import torch
from typing import List

class HuggingfaceEmbedder(BaseEmbedder):
    def __init__(self, model_name: str = "bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        
    def embed(self, text: str) -> List[float]:
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    @property
    def dimension(self) -> int:
        # Extracting embedding dimension from model's config
        return self.model.config.hidden_size
