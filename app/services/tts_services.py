import logging

import edge_tts
import uuid
import os
import asyncio
import requests

OUTPUT_DIR = "generated_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)
async def text_to_speech(text: str, voice: str = "zh-CN-XiaoyiNeural") -> str:
    """
    使用 Edge-TTS（微软 TTS）进行语音合成，返回音频文件路径。

    :param text: 要转换的文本
    :param voice: 语音角色（可选 zh-CN-XiaoyiNeural, zh-CN-YunjianNeural）
    :return: 生成的 MP3 语音文件路径
    """
    filename = f"{OUTPUT_DIR}/{uuid.uuid4()}.mp3"
    logging.info(f"开始语音转文字,文件名为:{filename}")
    logging.info(f"文字转语音内容为:{text}")
    tts = edge_tts.Communicate(text, voice)
    logging.info("开始语音合成")
    await tts.save(filename)
    logging.info("语音合成完成(这是异步处理逻辑)")
    return filename


