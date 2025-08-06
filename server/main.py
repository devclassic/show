from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from httpx import AsyncClient
import os
import uuid
import json
import asyncio
import shutil
from typing import List
from asr import model
import medgemma
import dotenv
import dicom2jpg
import glob

dotenv.load_dotenv()

apibase = os.getenv("BASE_API")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.post("/api/triage")
async def triage(file: UploadFile = File(...), text: str = Form(...)):
    """
    分诊导诊接口
    """
    token = os.getenv("TOKEN_ZHINENGDAOZHEN")
    os.path.exists("public/uploads/triage") or os.makedirs("public/uploads/triage")
    filename = os.path.join("public/uploads/triage", file.filename)
    with open(filename, "wb") as f:
        shutil.copyfileobj(file.file, f)

    async def upload_file(filepath, user):
        uploadurl = f"{apibase}/files/upload"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        data = {"user": user, "type": "XLSX"}
        with open(filepath, "rb") as f:
            files = {"file": (os.path.basename(filepath), f)}
            async with AsyncClient(timeout=None) as client:
                res = await client.post(
                    uploadurl, headers=headers, files=files, data=data
                )
        return res.json().get("id")

    async def run_workflow(fileid, text, user, response_mode="blocking"):
        workflow_url = f"{apibase}/workflows/run"
        headers = {
            "Authorization": f"Bearer {token}",
        }

        data = {
            "inputs": {
                "file": {
                    "transfer_method": "local_file",
                    "upload_file_id": fileid,
                    "type": "document",
                },
                "text": text,
            },
            "response_mode": response_mode,
            "user": user,
        }
        async with AsyncClient(timeout=None) as client:
            res = await client.post(workflow_url, headers=headers, json=data)
        return res.json()

    fileid = await upload_file(filename, "demo")
    result = await run_workflow(fileid, text, "demo")
    os.remove(filename)
    text = result.get("data").get("outputs").get("text")
    return {"success": True, "message": "分诊导诊成功", "data": text}


@app.post("/api/assist")
async def assist(request: Request):
    """
    辅助诊疗接口
    """
    data = await request.json()
    question = data.get("question")
    token = os.getenv("TOKEN_FUZHUZHENLIAO")
    url = f"{apibase}/chat-messages"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    data = {
        "user": "demo",
        "inputs": {},
        "query": question,
        "response_mode": "blocking",
    }
    async with AsyncClient(timeout=None) as client:
        res = await client.post(url, json=data, headers=headers)
        res = res.json()
    text = res.get("answer")
    return {"success": True, "message": "辅助诊疗成功", "data": text}


@app.post("/api/check")
async def check(request: Request):
    """
    内涵质控接口
    """
    token = os.getenv("TOKEN_NEIHANZHIKONG")

    async def run_workflow(type, content, user, response_mode="blocking"):
        workflow_url = f"{apibase}/workflows/run"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {
            "inputs": {
                "type": type,
                "content": content,
            },
            "response_mode": response_mode,
            "user": user,
        }
        async with AsyncClient(timeout=None) as client:
            res = await client.post(workflow_url, headers=headers, json=data)
        return res.json()

    data = await request.json()
    type = data.get("type")
    content = data.get("content")
    result = await run_workflow(type, content, "demo")
    text = result.get("data").get("outputs").get("text")
    return {"success": True, "message": "内涵质控成功", "data": text}


@app.post("/api/asr")
async def asrm(file: UploadFile = File(...)):
    """
    语音识别接口
    """
    os.path.exists("public/uploads/audio") or os.makedirs("public/uploads/audio")
    filename = os.path.join("public/uploads/audio", file.filename)
    with open(filename, "wb") as f:
        shutil.copyfileobj(file.file, f)

    res = await asyncio.get_event_loop().run_in_executor(None, model.generate, filename)

    os.remove(filename)
    return {"success": True, "message": "多人语音识别成功", "data": res}


@app.post("/api/asrg")
async def asrg(request: Request):
    """
    多人语音生成接口
    """
    data = await request.json()
    prompt = data.get("prompt")
    token = os.getenv("TOKEN_DUIHUASHENGCHENG")
    url = f"{apibase}/chat-messages"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    data = {
        "user": "demo",
        "inputs": {},
        "query": prompt,
        "response_mode": "blocking",
    }
    async with AsyncClient(timeout=None) as client:
        res = await client.post(url, json=data, headers=headers)
        res = res.json()
    text = res.get("answer")
    return {"success": True, "message": "多人语音生成成功", "data": text}


@app.post("/api/form")
async def form(request: Request):
    """
    语音表单接口
    """
    data = await request.json()
    prompt = data.get("prompt")
    token = os.getenv("TOKEN_YUYINBIAODAN")
    url = f"{apibase}/chat-messages"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    data = {
        "user": "demo",
        "inputs": {},
        "query": prompt,
        "response_mode": "blocking",
    }
    async with AsyncClient(timeout=None) as client:
        res = await client.post(url, json=data, headers=headers)
        res = res.json()
    text = res.get("answer")
    return {"success": True, "message": "语音拆分成功", "data": text}


@app.post("/api/updcm")
async def updcm(files: List[UploadFile] = File([])):
    """
    上传DCM文件接口
    """
    basedir = "public/uploads/dcm/"
    rd = str(uuid.uuid4())
    updir = basedir + "endcm_" + rd
    downdir = basedir + "dedcm_" + rd
    os.path.exists(updir) or os.makedirs(updir)

    for file in files:
        filename = os.path.join(updir, f"{file.filename}.dcm")
        with open(filename, "wb") as f:
            shutil.copyfileobj(file.file, f)

    try:
        dicom2jpg.dicom2png(origin=updir, target_root=downdir, multiprocessing=False)
        paths = glob.glob(downdir + "/**/*.png", recursive=True)
        images = []
        for path in paths:
            images.append(path.replace("\\", "/").replace("public/", "/"))
        return {
            "success": True,
            "message": "上传DCM成功",
            "data": {"images": images, "paths": paths},
        }
    except:
        return {"success": False, "message": "处理DCM失败"}


@app.post("/api/init-image-model")
async def init_image_model():
    medgemma.init()
    return {"success": True, "message": "初始化影像模型成功"}


@app.post("/api/uninit-image-model")
async def uninit_image_model():
    medgemma.uninit()
    return {"success": True, "message": "卸载影像模型成功"}


@app.post("/api/is-image-model-init")
async def is_image_model_init():
    return {
        "success": True,
        "message": "影像模型是否初始化",
        "data": medgemma.is_init(),
    }


@app.post("/api/image")
async def image(
    files: List[UploadFile] = File([]),
    text: str = Form(),
    history: str = Form(),
    paths: str = Form(""),
):
    """
    影像识别接口
    """
    os.path.exists("public/uploads/temp") or os.makedirs("public/uploads/temp")
    images = []
    for file in files:
        _, ext = os.path.splitext(file.filename)
        filename = os.path.join("public/uploads/temp", f"{uuid.uuid4()}{ext}")
        with open(filename, "wb") as f:
            shutil.copyfileobj(file.file, f)
            images.append(filename)

    messages = json.loads(history)
    msg = {"role": "user", "content": []}

    for img in images:
        msg["content"].append({"type": "image", "image": img})

    paths = paths.split(",") if paths.strip() else []
    for path in paths:
        msg["content"].append({"type": "image", "image": path})

    msg["content"].append({"type": "text", "text": text})
    messages.append(msg)

    result = await asyncio.get_event_loop().run_in_executor(
        None, medgemma.output, messages
    )

    messages.append(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": result,
                },
            ],
        }
    )

    return {
        "success": True,
        "message": "影像识别成功",
        "data": {"text": result, "history": messages},
    }


app.mount("/", StaticFiles(directory="public", html=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
