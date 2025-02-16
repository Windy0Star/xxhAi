from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import logging
import tempfile
import os
from app.services.community_services import convert_mp3_to_wav, asr_process, nlp_process, tts_process

router = APIRouter()

# 启用日志记录
logging.basicConfig(level=logging.INFO)


@router.post("/dialog", summary="语音对话", tags=["对话"])
async def voice_dialog(file: UploadFile = File(...)):
    """
    语音对话 API：
    - **输入**: 语音文件 (MP3 / WAV)
    - **输出**:
      - `speech.mp3`: 直接返回 MP3 音频文件
    """
    try:
        logging.info(f"📥 接收到语音文件: {file.filename}")

        # 读取音频数据
        audio_data = await file.read()
        file_extension = file.filename.split(".")[-1].lower()

        # 仅支持 MP3 / WAV
        if file_extension not in ["mp3", "wav"]:
            raise HTTPException(status_code=400, detail="仅支持 MP3 / WAV 格式的音频")

        # ✅ 统一 MP3 和 WAV 处理
        if file_extension == "mp3":
            wav_path = await convert_mp3_to_wav(audio_data)
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
                temp_wav.write(audio_data)
                wav_path = temp_wav.name

        logging.info(f"🎤 WAV 文件路径: {wav_path}")

        # ✅ 1. ASR 语音识别（使用 SiliconFlow API）
        recognized_text = await asr_process(wav_path)
        logging.info(f"🎙️ 语音识别结果: {recognized_text}")

        # ✅ 2. NLP 处理
        response_text = await nlp_process(recognized_text)
        logging.info(f"🤖 NLP 生成的回答: {response_text}")

        # ✅ 3. TTS 语音合成
        speech_mp3 = await tts_process(response_text)
        logging.info(f"🎵 语音合成文件: {speech_mp3}")

        # ✅ 清理临时文件
        os.remove(wav_path)

        # ✅ **返回完整 MP3 文件**
        return FileResponse(speech_mp3, media_type="audio/mpeg", filename="speech.mp3")

    except Exception as e:
        logging.error(f"❌ 发生错误: {str(e)}")

