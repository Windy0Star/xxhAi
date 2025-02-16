import requests
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# ✅ 启用日志
logging.basicConfig(level=logging.INFO)

# API 端点
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"

# API 认证 Token
API_TOKEN = "sk-dgrfsbapqcozsqzjqsyhyvdddwbhvihsximwvmhjiaftwnzq"

@app.post("/asr")
async def asr(file: UploadFile = File(...)):
    """ 接收前端上传的 MP3/WAV 文件并调用 SiliconFlow 语音识别 API """

    try:
        logging.info(f"📂 接收到文件: {file.filename}")

        # ✅ 1. 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(await file.read())  # ✅ 读取上传的音频文件
            temp_audio_path = temp_audio.name

        logging.info(f"📝 临时文件路径: {temp_audio_path}")

        # ✅ 2. 设置请求头
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        # ✅ 3. 准备文件数据
        with open(temp_audio_path, "rb") as audio_file:
            files = {"file": (file.filename, audio_file, "audio/wav")}

            logging.info("🚀 发送请求到 SiliconFlow 语音识别 API...")
            response = requests.post(SILICONFLOW_API_URL, headers=headers, files=files, data={"model": "FunAudioLLM/SenseVoiceSmall"})

        # ✅ 4. 删除临时文件
        try:
            os.remove(temp_audio_path)
            logging.info("🗑️ 删除临时文件成功！")
        except Exception as e:
            logging.warning(f"⚠️ 删除临时文件失败: {e}")

        # ✅ 5. 解析 API 响应
        logging.info(f"🔍 API 响应状态码: {response.status_code}")
        logging.info(f"🔍 API 响应内容: {response.text}")

        result = response.json()
        return JSONResponse(content=result)

    except requests.exceptions.RequestException as req_err:
        logging.error(f"❌ API 请求错误: {req_err}")
        return JSONResponse(content={"error": "API 请求失败"}, status_code=500)

    except requests.exceptions.JSONDecodeError:
        logging.error("❌ 无法解析 API 响应")
        return JSONResponse(content={"error": "无法解析语音识别 API 响应"}, status_code=500)

    except Exception as e:
        logging.error(f"❌ 发生未知错误: {e}")
        return JSONResponse(content={"error": f"内部错误: {str(e)}"}, status_code=500)
