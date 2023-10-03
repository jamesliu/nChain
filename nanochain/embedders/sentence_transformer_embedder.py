from sentence_transformers import SentenceTransformer

models = {"all-MiniLM-L6-v2":"120MB", "all-mpnet-base-v2":"420MB", "paraphrase-MiniLM-L6-v2":"120MB"}
class SentenceTransformerEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the embedder with a specific Sentence Transformer model.
        
        Args:
        - model_name (str): Name of the pre-trained Sentence Transformer model to use.
        """
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        """
        Generate an embedding for the given text.
        
        Args:
        - text (str): The text to be embedded.
        
        Returns:
        - list: The embedding vector.
        """
        return self.model.encode([text])[0]
