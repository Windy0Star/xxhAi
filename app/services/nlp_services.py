import logging
import os
import openai  # DeepSeek API 兼容 OpenAI SDK
from openai import OpenAI
# 配置 DeepSeek API Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your_api_key_here")
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

SLI_API_URL="https://api.siliconflow.cn/v1"
SLI_API_KEY= "sk-dgrfsbapqcozsqzjqsyhyvdddwbhvihsximwvmhjiaftwnzq"
logging.basicConfig(level=logging.INFO)
async def generate_response_SLI(prompt: str, model: str = "deepseek-chat"):
    """
    调用 DeepSeek API 进行 NLP 处理（流式返回）。
    """
    print("开始调用api")
    logging.info(f"开始推理，用户推理内容为:{prompt}")
    try:
        client = OpenAI(api_key=SLI_API_KEY, base_url="https://api.siliconflow.cn/v1")
        response = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-V2.5',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True  # ✅ 启用流式返回
        )
        logging.info("请求结束开始读取流式数据")
        # 逐步读取流式数据
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                print(content)
                yield content  # ✅ 逐块返回数据
    except Exception as e:
        yield f"DeepSeek API 调用失败: {str(e)}"
    logging.info("推理调用结束")
