from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from configs import Configs
from paths import Paths
from litgpt import LLM

class LLMHandler:

    # Generate an answer using the huggingface pipeline.
    def generate_answer_hf(self, prompt):
        print(f"Generating answer using model: {Configs.LLM_MODEL}, method HUGGINFACE PIPELINE")
        model = AutoModelForCausalLM.from_pretrained(Configs.LLM_MODEL, cache_dir=Paths.LLM_PATH)
        tokenizer = AutoTokenizer.from_pretrained(Configs.LLM_TOKENIZER, cache_dir=Paths.LLM_PATH)

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        generator = pipeline(
            task=Configs.LLM_TASK,
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=Configs.LLM_MAX_NEW_TOKENS,
            temperature=Configs.LLM_TEMP,
            return_full_text=False
        )

        return generator(prompt)[0]["generated_text"]

    # Generate an answer using the LitGPT
    def generate_answer_litgpt(self, prompt):
        print(f"Generating answer using model: {Configs.LLM_MODEL}, method LITGPT")
        llm = LLM.load(Configs.LLM_MODEL)
        text = llm.generate("Fix the spelling: Every fall, the familly goes to the mountains.")
        return text