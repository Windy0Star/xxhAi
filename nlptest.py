import asyncio
import speech_recognition as sr
from openai import OpenAI
import requests
import os
import uuid
import edge_tts
import mp3towav
SLI_API_KEY= "sk-dgrfsbapqcozsqzjqsyhyvdddwbhvihsximwvmhjiaftwnzq"

def generate_response_SLI(prompt: str, model: str = "deepseek-chat"):
    """
    调用 DeepSeek API 进行自然语言处理（NLP）。

    :param prompt: 用户输入的文本
    :param model: 选择的 DeepSeek 语言模型，默认是 "deepseek-chat"
    :return: DeepSeek 生成的文本
    """
    try:
        client = OpenAI(api_key=SLI_API_KEY, base_url="https://api.siliconflow.cn/v1")
        response = client.chat.completions.create(
            # model='deepseek-ai/DeepSeek-V3',
            model= 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
            messages=[
                {'role': 'user',
                 'content': prompt}
            ],
            stream=True
        )

        for chunk in response:
            print(chunk.choices[0].delta.content, end='')

    except Exception as e:
        return f"DeepSeek API 调用失败: {str(e)}"
def text2voice():

    url = "https://api.siliconflow.cn/v1/audio/speech"

    payload = {
        "model": "fishaudio/fish-speech-1.5",
        "input": "谢晓虎哥哥~，抱抱我",
        "voice": "fishaudio/fish-speech-1.5:alex",
        "response_format": "mp3",
        "sample_rate": 32000,
        "stream": True,
        "speed": 1,
        "gain": 0
    }
    headers = {
        "Authorization": "Bearer sk-dgrfsbapqcozsqzjqsyhyvdddwbhvihsximwvmhjiaftwnzq",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
def voice_get():
    url = "https://api.siliconflow.cn/v1/audio/transcriptions"

    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nFunAudioLLM/SenseVoiceSmall\r\n-----011000010111000001101001--\r\n\r\n"
    headers = {
        "Authorization": SLI_API_KEY,
        "Content-Type": "multipart/form-data"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_audio")  # 生成绝对路径
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def text_to_speech(text: str, voice: str = "zh-CN-XiaoyiNeural") -> str:
    """
    使用 Edge-TTS（微软 TTS）进行语音合成，返回音频文件路径。

    :param text: 要转换的文本
    :param voice: 语音角色（可选 zh-CN-XiaoyiNeural, zh-CN-YunjianNeural）
    :return: 生成的 MP3 语音文件路径
    """
    filename = f"{OUTPUT_DIR}/{uuid.uuid4()}.mp3"
    print(filename)

    tts = edge_tts.Communicate(text, voice)
    print("开始语音合成")
    await tts.save(filename)
    print("语音合成完成")
    return filename

def asr(wavfile):
    recognizer = sr.Recognizer()

    try:

        # API 端点
        url = "https://api.siliconflow.cn/v1/audio/transcriptions"

        # API 认证 Token
        api_token = "sk-dgrfsbapqcozsqzjqsyhyvdddwbhvihsximwvmhjiaftwnzq"

        # 需要上传的音频文件（替换成你的文件路径）
        audio_file_path = "converted.wav"

        # 设置请求头
        headers = {
            "Authorization": f"Bearer {api_token}"
        }

        # 准备文件数据
        files = {
            "file": ("converted.wav", open(audio_file_path, "rb"), "audio/wav")
        }

        # 发送 POST 请求
        response = requests.post(url, headers=headers, files=files, data={"model": "FunAudioLLM/SenseVoiceSmall"})

        # 输出结果
        print(response.json())


    except sr.UnknownValueError:
        return "无法识别语音"

    except sr.RequestError as e:
        return f"请求语音识别服务失败: {e}"
# if __name__ == "__main__":
    # generate_response_SLI("请帮我设计个年终晚会发言稿")
    # result = asr("converted.wav")
    # print(f"识别结果: {result}")  # 打印输出
    # asyncio.run(text_to_speech("你好，这是一个测试"))    #注意，Fastapi要用await调用即可
import asyncio
async def test_tts():
    tts = edge_tts.Communicate("谢晓虎哥哥~，抱抱我", "zh-CN-XiaoyiNeural")
    await tts.save("test.mp3")
#
asyncio.run(test_tts())

