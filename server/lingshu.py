from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch


# We recommend enabling flash_attention_2 for better acceleration and memory saving, especially in multi-image and video scenarios.
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    "cache",
    # "lingshu-medical-mllm/Lingshu-7B",
    torch_dtype=torch.bfloat16,
    # attn_implementation="flash_attention_2",
    device_map="cuda",
)

processor = AutoProcessor.from_pretrained(
    "cache",
    # "lingshu-medical-mllm/Lingshu-7B",
    use_fast=True,
)

# model.save_pretrained("cache")
# processor.save_pretrained("cache")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "用中文回答用户问题"},
        ],
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "你是端点科技医疗影像助手"},
        ],
    },
    {"role": "assistant", "content": [{"type": "text", "text": "AI回答"}]},
]


def output(messages):
    # Preparation for inference
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to(model.device)

    # Inference: Generation of the output
    generated_ids = model.generate(**inputs, max_new_tokens=128000)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )
    text = output_text[0]

    return text
