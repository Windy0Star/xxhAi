import uuid

import edge_tts
import logging
import tempfile
import os
import requests
from pydub import AudioSegment

# 🔥 启用日志记录
logging.basicConfig(level=logging.INFO)

API_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"
API_TOKEN = "sk-dgrfsbapqcozsqzjqsyhyvdddwbhvihsximwvmhjiaftwnzq"
OUTPUT_DIR = "generated_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)
async def convert_mp3_to_wav(mp3_data: bytes) -> str:
    """
    使用 pydub 将 MP3 转换为 WAV（16-bit PCM）
    """
    try:
        logging.info("🚀 开始 MP3 转 WAV 处理...")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
            temp_mp3.write(mp3_data)
            temp_mp3_path = temp_mp3.name  # ✅ 生成临时 MP3 文件路径

        wav_path = temp_mp3_path.replace(".mp3", ".wav")
        logging.info(f"📝 MP3 文件路径: {temp_mp3_path}")
        logging.info(f"🎯 目标 WAV 文件路径: {wav_path}")

        # ✅ 确保输出 WAV 为 16-bit PCM 格式
        try:
            audio = AudioSegment.from_mp3(temp_mp3_path)
        except Exception as decode_err:
            raise ValueError(f"MP3 解码失败: {decode_err}")

        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        audio.export(wav_path, format="wav")

        os.remove(temp_mp3_path)  # ✅ 删除临时 MP3 文件
        logging.info("✅ MP3 转换为 WAV 成功！")

        if not os.path.exists(wav_path):  # 确保转换成功
            raise ValueError("WAV 文件转换失败")

        return wav_path  # ✅ 返回 WAV 文件路径

    except Exception as e:
        logging.error(f"❌ MP3 转换失败: {e}")
        raise

async def send_to_siliconflow_api(wav_path: str) -> str:
    """
    将 WAV 音频文件发送到 SiliconFlow 语音识别 API 并返回识别文本
    """
    try:
        logging.info(f"📡 发送音频文件到 SiliconFlow API: {wav_path}")

        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }

        with open(wav_path, "rb") as audio_file:
            files = {
                "file": (wav_path, audio_file, "audio/wav")
            }
            data = {"model": "FunAudioLLM/SenseVoiceSmall"}

            response = requests.post(API_URL, headers=headers, files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            recognized_text = result.get("text", "语音识别成功，但未返回文本")
            logging.info(f"📝 语音识别结果: {recognized_text}")
            return recognized_text
        else:
            error_message = f"语音识别失败: {response.text}"
            logging.error(error_message)
            raise ValueError(error_message)

    except Exception as e:
        logging.error(f"❌ 请求语音识别服务失败: {e}")
        raise

async def asr_process(wav_path: str) -> str:
    """
    语音识别（通过 SiliconFlow API 处理）
    """
    return await send_to_siliconflow_api(wav_path)

async def nlp_process(recognized_text: str) -> str:
    """
    文本生成（NLP）
    """
    try:
        logging.info("📝 进行 NLP 推理...")
        # 这里可以换成更高级的 NLP 逻辑
        response_text = f"你的问题是: {recognized_text}"
        logging.info(f"🤖 NLP 生成的回答: {response_text}")

        return response_text

    except Exception as e:
        logging.error(f"❌ NLP 处理失败: {e}")
        raise

async def tts_process(response_text: str) -> str:
    """
    语音合成（TTS）
    """
    try:
        logging.info("🔊 进行语音合成...")
        filename = f"{OUTPUT_DIR}/{uuid.uuid4()}.mp3"

        # 这里可以接入更强大的 TTS 引擎
        print("开始语音合成")
        print(response_text)
        tts = edge_tts.Communicate(response_text, "zh-CN-XiaoyiNeural")
        await tts.save(filename)
        print("语音合成完成")
        logging.info(f"🎵 语音合成文件: {filename}")

        return filename

    except Exception as e:
        logging.error(f"❌ TTS 处理失败: {e}")
        raise
