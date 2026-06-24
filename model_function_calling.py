import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig

def build_llm_model():
    model_id = "Qwen/Qwen2.5-3B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    bnb_config = BitsAndBytesConfig(
        load_in_4bit = True,
        bnb_4bit_quant_type = "nf4"
    )


    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config = bnb_config,
        device_map = "auto",

        torch_dtype = torch.float16
    )
    return model, tokenizer

def call_llama_with_chat_template(model, tokenizer, messages, tools):
    prompt = tokenizer.apply_chat_template(
        messages,
        tools = tools,
        tokenize = False,
        add_generation_prompt = True 
    )

    inputs = tokenizer(prompt, return_tensors = "pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens = 200,
        do_sample = False,
        pad_token_id = tokenizer.eos_token_id
    )

    generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    generated_text = tokenizer.decode(generated_tokens, skip_special_tokens = True).strip()

    return generated_text


# def call_llama_with_chat_template(messages, tools):

