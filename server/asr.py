from funasr import AutoModel

model = AutoModel(
    disable_update=True,
    model="paraformer-zh",
    vad_model="fsmn-vad",
    punc_model="ct-punc",
    spk_model="cam++",
)
