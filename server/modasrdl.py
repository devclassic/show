from modelscope.hub.snapshot_download import snapshot_download

# 模型列表及对应的ModelScope仓库地址
model_repos = {
    "paraformer-zh": "iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    "fsmn-vad": "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    "ct-punc": "iic/punc_ct-transformer_cn-en-common-vocab471067-large",
    "cam++": "iic/speech_campplus_sv_zh-cn_16k-common",
}

# 下载所有模型到本地目录（如./local_models）
for model_name, repo_id in model_repos.items():
    snapshot_download(repo_id, cache_dir=f"./models/funasr/{model_name}")
