from fastapi import FastAPI
from routers import asr, nlp, tts,community
import uvicorn

app = FastAPI(title="AI 语音助手 API", version="1.0")

# 注册路由
app.include_router(asr.router, prefix="/asr", tags=["语音识别"])
app.include_router(nlp.router, prefix="/nlp", tags=["自然语言处理"])
app.include_router(tts.router, prefix="/tts", tags=["语音合成"])
app.include_router(community.router, prefix="/community", tags=["语音对话"])


@app.get("/")
def read_root():
    return {"message": "AI 语音助手服务已启动"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8083)