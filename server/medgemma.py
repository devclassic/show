from transformers import AutoProcessor, AutoModelForImageTextToText, BitsAndBytesConfig
import torch
import gc

model = None
processor = None


def init():
    global model
    global processor

    model_id = "models/medgemma-4b-it"

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        # llm_int8_enable_fp32_cpu_offload=True,
    )

    model = AutoModelForImageTextToText.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        attn_implementation="sdpa",
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    processor = AutoProcessor.from_pretrained(model_id, use_fast=True)


def uninit():
    global model
    global processor
    model = None
    processor = None
    torch.cuda.empty_cache()
    gc.collect()


def is_init():
    return model is not None and processor is not None


messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "你是一位全科医疗影像专家，你的任务是根据输入的影像和文本描述，输出专业的诊断结果。",
            }
        ],
    },
    {
        "role": "user",
        "content": [
            {"type": "image", "image": "1.jpg"},
            {"type": "text", "text": "分析一下这张片子"},
        ],
    },
]


def output(messages):
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device, dtype=torch.bfloat16)

    input_len = inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = model.generate(**inputs, max_new_tokens=4096, do_sample=False)
        generation = generation[0][input_len:]

    decoded = processor.decode(generation, skip_special_tokens=True)
    return decoded
