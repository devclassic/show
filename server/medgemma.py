from transformers import pipeline

pipe = pipeline(
    task="image-text-to-text",
    model="models/medgemma-4b-it",
    torch_dtype="auto",
    device_map="auto",
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
