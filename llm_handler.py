from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from configs import Configs


# This class handles the LLM model, it loads the model and tokenizer, generates the system propmt and also generates answers using the model.
class LLMHandler:

    # Constructor
    def __init__(self):
        print(f"Loading LLM model: {Configs.LLM_MODEL}")
        self.model = AutoModelForCausalLM.from_pretrained(Configs.LLM_MODEL, cache_dir=Configs.LLM_PATH)
        self.tokenizer = AutoTokenizer.from_pretrained(Configs.LLM_TOKENIZER, cache_dir=Configs.LLM_PATH)
        self.generator = pipeline(
            task=Configs.LLM_TASK,
            model=self.model,
            tokenizer=self.tokenizer
        )

        # Set the padding token from the tokenizer to the model, this needs to be done manually else we get an annoying warning from HuggingFace.
        self.model.generation_config.pad_token_id = self.tokenizer.pad_token_id


    # Generate an answer using the huggingface pipeline.
    def generate_answer_hf_pipeline(self, prompt):
        print(f"Generating answer using model: {Configs.LLM_MODEL}, method HUGGINFACE PIPELINE")

        # Pass generation arguments here
        output = self.generator(
            prompt,
            max_new_tokens=Configs.LLM_MAX_NEW_TOKENS,
            do_sample=Configs.LLM_RANDOM,
            temperature=Configs.LLM_TEMP,
            return_full_text=Configs.LLM_RETURN_FULL_TEXT
        )

        return output[0]['generated_text']


    # Generate an answer using the classic method
    def generate_answer_hf_tokenizer(self, prompt):
        print(f"Generating answer using model: {Configs.LLM_MODEL}, method HUGGINGFACE TOKENIZER")

        # Tokenize the prompt
        inputs = self.tokenizer(prompt, return_tensors="pt")

        # Generate the output from the model
        output = self.model.generate(**inputs, 
            max_new_tokens=Configs.LLM_MAX_NEW_TOKENS,
            do_sample=Configs.LLM_RANDOM,
            temperature=Configs.LLM_TEMP)

        return self.tokenizer.decode(output[0], skip_special_tokens=True)


    # Generate a prompt for the LLM model using the query and the results from the database.
    def generate_prompt(self, results, query):
        # If there are no results, or the score of the results are below the threshold, tell the LLM to tell the user to try again.
        if not results or results[0][1] < Configs.EMBEDDINGS_THRESHOLD:
            return "Follow this instruction, repeat after me and dont do anything else after: 'Couldn't find any document, please try again.'"

        # Generate a string with the documents and their scores.
        documents_str = "\n".join([f"Document: {doc.page_content}\n------------------------------" for doc, _ in results])
        return Configs.PROMPT_INSTRUCTION.format(documents=documents_str, question=query)

        """
        Document:
        asdadasdasdasdasdsad
        asdasdasdasdas
        dasdasd

        ------------------------------
        Document:
        asdadasdasdasdasdsad
        asdasdasdasdas
        dasdasd

        ------------------------------
        Document:
        asdadasdasdasdasdsad
        asdasdasdasdas
        dasdasd

        ------------------------------
        ocument:
        asdadasdasdasdasdsad
        asdasdasdasdas
        dasdasd

        ------------------------------
        
        """