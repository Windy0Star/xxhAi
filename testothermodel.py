SLI_API_KEY= "sk-dgrfsbapqcozsqzjqsyhyvdddwbhvihsximwvmhjiaftwnzq"

from openai import OpenAI
url = 'https://api.siliconflow.cn/v1/'
api_key = SLI_API_KEY

client = OpenAI(
    base_url=url,
    api_key=api_key
)

# 发送非流式输出的请求
messages = [
    {"role": "user", "content": "怎么酿造红酒？"}
]
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    messages=messages,
    stream=False,
    max_tokens=4096
)
content = response.choices[0].message.content
reasoning_content = response.choices[0].message.reasoning_content
print(reasoning_content)
# # Round 2
# messages.append({"role": "assistant", "content": content})
# messages.append({'role': 'user', 'content': "继续"})
# response = client.chat.completions.create(
#     model="deepseek-ai/DeepSeek-R1",
#     messages=messages,
#     stream=False
# )
