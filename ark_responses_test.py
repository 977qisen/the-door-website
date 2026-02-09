import os
from openai import OpenAI

# 从环境变量中获取API KEY
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
    # 使用 responses.create API
    # 注意：responses API 的 input 格式与 chat.completions 不同
    response = client.responses.create(
        model="doubao-vision-pro-32k-241028",  # 视觉理解模型
        input="你看见了什么？请描述这张图片。",  # 纯文本输入
        # 如果需要传图片，responses API 可能需要使用其他方式
        # 或者使用 chat.completions.create 更合适
    )
    
    print("=" * 50)
    print("模型回复：")
    print("=" * 50)
    print(response.output_text)
    print("=" * 50)
    
except Exception as e:
    print(f"请求出错：{e}")
    print("\n提示：如果需要同时传入图片和文本，建议使用 chat.completions.create API")
