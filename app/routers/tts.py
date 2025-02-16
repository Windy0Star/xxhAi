from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.tts_services import text_to_speech

router = APIRouter()

# ✅ 使用 Pydantic 定义请求体
class TTSRequest(BaseModel):
    text: str
    voice: str = "zh-CN-XiaoyiNeural"

@router.post("/synthesize", summary="中文文本转语音", tags=["TTS"])
async def synthesize_speech(request: TTSRequest):
    """
    中文文本转语音 API，返回 MP3 音频文件。

    - **text**: 需要合成的文本
    - **voice**: 语音角色（默认 `zh-CN-XiaoyiNeural`）
    - **返回**: MP3 音频文件
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="文本不能为空")

    audio_file = await text_to_speech(request.text, request.voice)

    if audio_file.endswith(".mp3"):
        return FileResponse(audio_file, media_type="audio/mpeg", filename="speech.mp3")
    else:
        raise HTTPException(status_code=500, detail="语音合成失败")
