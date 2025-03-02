import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.nlp_services import generate_response_SLI
from pydantic import BaseModel

router = APIRouter()
logging.basicConfig(level=logging.INFO)
class ChatRequest(BaseModel):
    prompt: str

@router.post("/chat", summary="自然语言处理", tags=["NLP"])
async def chat_with_deepseek(request: ChatRequest):
    """
    通过 DeepSeek API 进行 NLP 处理，支持流式返回。

    - **prompt**: 用户输入文本
    - **返回**: 实时返回 DeepSeek 生成的内容
    """

    async def event_stream():
        try:
            async for chunk in generate_response_SLI(request.prompt):
                yield chunk  # 逐步返回数据
        except Exception as e:
            yield f"DeepSeek API 调用失败: {str(e)}"

    return StreamingResponse(event_stream(), media_type="text/plain")  # 以流方式返回
