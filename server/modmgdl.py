import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# os.environ["HF_TOKEN"] = "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"

from huggingface_hub import snapshot_download

MODEL_ID = "google/medgemma-27b-it"

cached = snapshot_download(
    repo_id=MODEL_ID, resume_download=True, cache_dir="./models/medgemma-27b-it"
)
