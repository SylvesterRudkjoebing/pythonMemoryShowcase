import os
from transformers import pipeline

class llmObject:
    def __init__(self, path="../Llama-3.2-1B"):
        self.path = path
        self.pipe = None

    def load_model(self):
        # Check if the model path exists
        if not os.path.exists(self.path):
            print(f"Model path {self.path} not found. Download/get the Model and place in same folder as root folder")
            self.pipe = None
        else:
            self.pipe = pipeline(
                "text-generation",
                model=self.path,
            )

    def communicate(self, question, max_tokens=100):
        if self.pipe is None:
            # Return the question itself if model is not loaded
            return question
        else:
            return self.pipe(question, max_new_tokens=max_tokens)[0]["generated_text"]
