import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydub import AudioSegment
import tempfile
import os
import requests
import asyncio

router = APIRouter()
logging.basicConfig(level=logging.INFO)
API_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"
API_TOKEN = "sk-dgrfsbapqcozsqzjqsyhyvdddwbhvihsximwvmhjiaftwnzq"

async def convert_mp3_to_wav(mp3_data: bytes) -> str:
    """
    使用 pydub 将 MP3 转换为 WAV（16-bit PCM）
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
            temp_mp3.write(mp3_data)
            temp_mp3_path = temp_mp3.name

        wav_path = temp_mp3_path.replace(".mp3", ".wav")

        # ✅ 确保输出 WAV 为 16-bit PCM 格式
        audio = AudioSegment.from_mp3(temp_mp3_path)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        audio.export(wav_path, format="wav")

        os.remove(temp_mp3_path)  # ✅ 删除临时 MP3 文件

        if not os.path.exists(wav_path):  # 确保转换成功
            raise Exception("WAV 文件转换失败")

        return wav_path

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MP3 转换失败: {str(e)}")


async def send_to_siliconflow_api(wav_path: str):
    """
    将 WAV 音频文件发送到 SiliconFlow 语音识别 API 并返回结果
    """
    try:
        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }

        with open(wav_path, "rb") as audio_file:
            files = {
                "file": (wav_path, audio_file, "audio/wav")
            }
            data = {"model": "FunAudioLLM/SenseVoiceSmall"}
            logging.info("请求组装完成，向api接口发送Wav格式语音内容")
            response = requests.post(API_URL, headers=headers, files=files, data=data)

            if response.status_code == 200:
                result = response.json()
                logging.info(f"语音识别成功，内容为:{result}")

                yield result.get("text", "语音识别成功，但未返回文本")
            else:
                yield f"语音识别失败: {response.text}"

    except Exception as e:
        yield f"请求语音识别服务失败: {str(e)}"


@router.post("/recognize", summary="语音识别", tags=["语音识别"])
async def recognize_speech(file: UploadFile = File(...)):
    """
    上传音频文件进行语音识别，支持 MP3、WAV、流式音频。

    - **file**: 语音文件 (MP3、WAV)
    """
    try:
        logging.info(f"📥 接收到语音文件: {file.filename}")

        # 读取音频数据
        audio_data = await file.read()

        # 获取文件格式
        file_extension = file.filename.split(".")[-1].lower()

        # 仅支持 MP3 和 WAV
        if file_extension not in ["mp3", "wav"]:
            raise HTTPException(status_code=400, detail="仅支持 MP3 / WAV 格式的音频")

        # 如果是 MP3，则转换为 WAV
        if file_extension == "mp3":
            wav_path = await convert_mp3_to_wav(audio_data)
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
                temp_wav.write(audio_data)
                wav_path = temp_wav.name
        logging.info("格式校验及转换完成")
        # 以流式方式返回 ASR 识别内容
        async def streaming_response():
            try:
                async for chunk in send_to_siliconflow_api(wav_path):
                    yield chunk
            finally:
                os.remove(wav_path)  # ✅ 仅在数据流结束后删除文件

        return StreamingResponse(streaming_response(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
