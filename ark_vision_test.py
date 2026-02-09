import os
from openai import OpenAI

# 从环境变量中获取API KEY
# 配置方法见：https://www.volcengine.com/docs/82379/1399008
api_key = os.getenv('ARK_API_KEY')

if not api_key:
    print("错误：请设置环境变量 ARK_API_KEY")
    print("示例：export ARK_API_KEY='your-api-key-here'")
    exit(1)

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=api_key,
)

try:
    response = client.chat.completions.create(
        model="doubao-vision-pro-32k-241028",  # 视觉理解模型
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/ark_demo_img_1.png"
                        }
                    },
                    {
                        "type": "text",
                        "text": "你看见了什么？"
                    },
                ],
            }
        ]
    )
    
    print("=" * 50)
    print("模型回复：")
    print("=" * 50)
    print(response.choices[0].message.content)
    print("=" * 50)
    print(f"使用模型：{response.model}")
    print(f"Token使用：prompt={response.usage.prompt_tokens}, completion={response.usage.completion_tokens}")
    
except Exception as e:
    print(f"请求出错：{e}")
