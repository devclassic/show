from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from httpx import AsyncClient
import os
import shutil
from typing import List
import lingshu
from asr import model

apibase = "http://localhost:8080/v1"

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
    token = "app-fyeJMnOW042Mccwr2dsTTdb4"
    os.path.exists("uploads") or os.makedirs("uploads")
    filename = os.path.join("uploads", file.filename)
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
    print(fileid)
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
    token = "app-RWL2ZXbQoXKE524bFSmfRb28"
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
    token = "app-6klx0hvKgmvPcoScVA7CL2GY"

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


@app.post("/api/asrm")
async def asrm(file: UploadFile = File(...)):
    """
    多人语音识别接口
    """
    os.path.exists("uploads") or os.makedirs("uploads")
    filename = os.path.join("uploads", file.filename)
    with open(filename, "wb") as f:
        shutil.copyfileobj(file.file, f)
    res = model.generate(input=filename)
    os.remove(filename)
    return {"success": True, "message": "多人语音识别成功", "data": res}


@app.post("/api/asrg")
async def asrg(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    token = "app-8gtJR5XbwXB9FrpYuqpttMlc"
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
    data = await request.json()
    prompt = data.get("prompt")
    token = "app-j1f1vYJsSZTzXz0yIu4BMttA"
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


@app.post("/api/image")
async def image(files: List[UploadFile] = File([]), text: str = Form()):
    """
    影像识别接口
    """
    os.path.exists("uploads") or os.makedirs("uploads")
    images = []
    for file in files:
        filename = os.path.join("uploads", file.filename)
        with open(filename, "wb") as f:
            shutil.copyfileobj(file.file, f)
            images.append(filename)
    lingshu.set_message(images, text)
    return {"success": True, "message": "影像识别成功", "data": lingshu.output()}


@app.post("/api/image/reset")
async def image_reset():
    """
    影像识别接口重置
    """
    lingshu.reset_message()
    return {"success": True, "message": "影像识别重置成功", "data": True}


app.mount("/", StaticFiles(directory="public", html=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
