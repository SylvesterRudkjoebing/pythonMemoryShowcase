from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class llmObject:
    def __init__(self, path="/Users/sylvesterrudkjobing/Python projekter/showcaseAutobiographicalMemory/Llama-3.2-1B"):
        self.path = path
        self.pipe = None

    def load_model(self):
        self.pipe = pipeline(
            "text-generation",
            model=self.path,
        )

    def communicate(self, question, max_tokens=100):
        print(self.pipe(question, max_new_tokens=max_tokens)[0]["generated_text"])