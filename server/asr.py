from funasr import AutoModel

model = AutoModel(
    disable_update=True,
    model="./models/funasr/paraformer-zh/iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    vad_model="./models/funasr/fsmn-vad/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    punc_model="./models/funasr/ct-punc/iic/punc_ct-transformer_cn-en-common-vocab471067-large",
    spk_model="./models/funasr/cam++/iic/speech_campplus_sv_zh-cn_16k-common",
)
