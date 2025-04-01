from factory_sdk.dto.model import ModelInstance
from transformers import AutoModelForCausalLM, AutoProcessor, AutoTokenizer, AutoConfig
import os
from peft import get_peft_model
from accelerate import init_empty_weights
from peft import (
    get_peft_model,
    PeftModelForCausalLM,
    prepare_model_for_kbit_training,
)
from rich import print


def load_empty_model(path):
    config = AutoConfig.from_pretrained(path)
    with init_empty_weights():
        return AutoModelForCausalLM.from_config(config)


def load_model(path, peft_config, bnb_config, dtype, device="cuda"):
    # check if there is a preprocessor_config.json file
    hash_preprocessor_config = os.path.isfile(
        os.path.join(path, "preprocessor_config.json")
    )

    # attention_implementation="flash"
    model = AutoModelForCausalLM.from_pretrained(
        path,
        quantization_config=bnb_config,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )

    if peft_config is None:
        peft_model = model

    else:

        peft_model = get_peft_model(
            model,
            peft_config,
        )

    if hash_preprocessor_config:
        processor = AutoProcessor.from_pretrained(path)
        return ModelInstance(
            model=peft_model,
            tokenizer=processor.tokenizer,
            processor=processor,
        )
    else:
        tokenizer = AutoTokenizer.from_pretrained(path)
        return ModelInstance(
            model=peft_model,
            tokenizer=tokenizer,
            processor=None,
        )
    
def load_model_for_evaluation(path, init_path, bnb_config, dtype, device="cuda"):
    model = AutoModelForCausalLM.from_pretrained(
        path,
        device_map="auto",
        torch_dtype=dtype,
        quantization_config=bnb_config,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )

    peft_model = PeftModelForCausalLM.from_pretrained(
        model, init_path, is_trainable=False,
    )


    peft_model.eval()

    has_preprocessor_config = os.path.isfile(
        os.path.join(path, "preprocessor_config.json")
    )

    if has_preprocessor_config:
        processor = AutoProcessor.from_pretrained(path)
        return ModelInstance(
            model=peft_model,
            tokenizer=processor.tokenizer,
            processor=processor,
        )
    else:
        tokenizer = AutoTokenizer.from_pretrained(path)
        return ModelInstance(
            model=peft_model,
            tokenizer=tokenizer,
            processor=None,
        )


def load_model_for_training(path, init_path, bnb_config, dtype, device="cuda"):

    model = AutoModelForCausalLM.from_pretrained(
        path,
        device_map="auto",
        torch_dtype=dtype,
        quantization_config=bnb_config,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )

    if bnb_config is not None:
        model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)

    peft_model = PeftModelForCausalLM.from_pretrained(
        model, init_path, is_trainable=True
    )

    has_preprocessor_config = os.path.isfile(
        os.path.join(path, "preprocessor_config.json")
    )

    if has_preprocessor_config:
        processor = AutoProcessor.from_pretrained(path)
        return ModelInstance(
            model=peft_model,
            tokenizer=processor.tokenizer,
            processor=processor,
        )
    else:
        tokenizer = AutoTokenizer.from_pretrained(path)
        return ModelInstance(
            model=peft_model,
            tokenizer=tokenizer,
            processor=None,
        )


def detect_response_template(tokenizer) -> str:
    test_message = "Input Test"
    test_output = "Output Test"

    prompt1 = tokenizer.apply_chat_template(
        [
            {"role": "user", "content": test_message},
            {"role": "assistant", "content": test_output},
        ],
        tokenize=False,
        add_generation_prompt=True,
    )
    prompt2 = tokenizer.apply_chat_template(
        [
            {"role": "user", "content": test_message},
            {"role": "assistant", "content": test_output},
        ],
        tokenize=False,
        add_generation_prompt=False,
    )

    prompt_length = len(prompt2)
    template = prompt1[prompt_length:]

    print(f"Detected response template: {template}")

    if "<|assistant|>" in prompt1 or "<|assistant|>" in prompt2:
        template = "<|assistant|>"

    print(f"Detected response template: {template}")

    return template
