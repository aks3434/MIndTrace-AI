import numpy as np

class EmbeddingEncoder:
    def __init__(self, model):
        self.model = model  # sentence-transformers / OpenAI / local

    def encode(self, text: str) -> np.ndarray:
        return np.array(self.model.encode(text))

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
