from openai import OpenAI
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
            model= 'deepseek-ai/DeepSeek-V3',
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

generate_response_SLI("我想知道卤肉怎么做，50字以内")