from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class llmObject:
    def __init__(self, path="/Users/sylvesterrudkjobing/Python projekter/Llama-3.2-1B"):
        self.path = path
        self.pipe = None

    def load_model(self):
        self.pipe = pipeline(
            "text-generation",
            model=self.path,
        )

    def communicate(self, question, max_tokens=100):
        print(self.pipe(question, max_new_tokens=max_tokens)[0]["generated_text"])

# Til eksperimentering:

# path="/Users/sylvesterrudkjobing/Python projekter/Llama-3.2-1B"

# pipe = pipeline(
#             "text-generation",
#             model=path,
#         )
# question = "Skriv disse vennehistorier: 1: Du og Gert mødtes ved et tilfældigt møde på gaden, 2: Gert introducerede dig til Rikke til Thomas' Fødselsdagsfest, 3: Rikke introducerede dig til Kasper til basketturneringen samme år Harden blev MVP"

# print(pipe(question, max_new_tokens=30)[0]["generated_text"])