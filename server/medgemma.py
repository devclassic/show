from transformers import pipeline
import torch

pipe = pipeline(
    task="image-text-to-text",
    model="models/medgemma-4b-it",
    device_map="auto",
    torch_dtype=torch.float16,
    model_kwargs={
        "load_in_4bit": True,
        "bnb_4bit_compute_dtype": torch.float16,
        "bnb_4bit_use_double_quant": True,
        "bnb_4bit_quant_type": "nf4",
    },
)

messages = [
    {"role": "system", "content": [{"type": "text", "text": "你是一位医疗影像专家"}]},
    {
        "role": "user",
        "content": [
            {"type": "image", "image": "111.jpg"},
            {"type": "text", "text": "分析一下这张片子"},
        ],
    },
]


def output(messages):
    output = pipe(text=messages, max_new_tokens=10000)
    result = output[0]["generated_text"][-1]["content"]
    return result
