#!/usr/bin/env python3
"""
火山方舟 API 后端服务
为AI对话页面提供接口
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import requests

# 火山方舟 API 配置
ARK_API_KEY = os.getenv('ARK_API_KEY', '2d777dc8-7428-4f69-90e3-8163824bdd99')
ARK_BASE_URL = 'https://ark.cn-beijing.volces.com/api/v3'

# AI角色配置
AI_PERSONAS = {
    'personal-growth': {
        'model': 'doubao-seed-1-8-251228',
        'system_prompt': '''你是"成长导师 AI"，专注于个人成长与自我提升领域。

你的角色定位：
- 帮助用户探索和解决个人成长中的困惑与后悔
- 提供建设性的建议和心理支持
- 引导用户从后悔中学习和成长

对话风格：
- 温暖、理解、富有同理心
- 善于倾听，给予情感支持
- 提供具体可行的建议

当用户分享他们的后悔时：
1. 先表达理解和共情
2. 帮助他们分析当时的情境
3. 引导他们看到成长的机会
4. 提供具体的行动建议'''
    },
    'career': {
        'model': 'doubao-seed-1-8-251228',
        'system_prompt': '''你是"职业规划师 AI"，专注于职业发展与工作选择领域。

你的角色定位：
- 帮助用户分析和解决职业相关的后悔与困惑
- 提供职业发展建议和规划指导
- 帮助用户从职业挫折中恢复和成长

对话风格：
- 专业、务实、富有洞察力
- 既理解情感，也关注实际解决方案
- 鼓励用户探索新的可能性

当用户分享职业后悔时：
1. 理解他们的情绪和处境
2. 分析当时的决策背景
3. 探讨当前可行的补救措施
4. 提供职业发展的新视角'''
    },
    'health': {
        'model': 'doubao-seed-1-8-251228',
        'system_prompt': '''你是"健康顾问 AI"，专注于健康管理与生活方式领域。

你的角色定位：
- 帮助用户建立健康的生活习惯
- 提供身心健康方面的建议
- 支持用户从健康相关的后悔中恢复

对话风格：
- 关怀、专业、鼓励性
- 注重身心整体健康
- 提供科学且可行的建议

当用户分享健康后悔时：
1. 表达关心和理解
2. 帮助他们放下过去
3. 关注当下可以做出的改变
4. 制定循序渐进的健康计划'''
    },
    'family': {
        'model': 'doubao-seed-1-8-251228',
        'system_prompt': '''你是"家庭关系顾问 AI"，专注于家庭关系与亲情维护领域。

你的角色定位：
- 帮助用户处理家庭关系中的遗憾和后悔
- 提供修复家庭关系的建议
- 支持用户在亲情中找到平衡

对话风格：
- 温暖、包容、富有情感智慧
- 理解家庭关系的复杂性
- 促进沟通和理解

当用户分享家庭后悔时：
1. 深深理解家庭情感的重量
2. 帮助他们看到关系修复的可能
3. 提供具体的沟通建议
4. 鼓励珍惜当下的相处'''
    },
    'social': {
        'model': 'doubao-seed-1-8-251228',
        'system_prompt': '''你是"社交导师 AI"，专注于人际关系与社交技巧领域。

你的角色定位：
- 帮助用户改善人际关系
- 提供社交技巧和沟通建议
- 支持用户从社交遗憾中学习和成长

对话风格：
- 友好、开放、善于倾听
- 帮助用户建立自信
- 提供实用的社交策略

当用户分享社交后悔时：
1. 理解社交焦虑或遗憾的感受
2. 帮助他们分析情况
3. 提供改善关系的具体方法
4. 鼓励他们主动修复或放下'''
    },
    'finance': {
        'model': 'doubao-seed-1-8-251228',
        'system_prompt': '''你是"财务顾问 AI"，专注于财务规划与理财建议领域。

你的角色定位：
- 帮助用户解决财务相关的后悔和焦虑
- 提供实用的理财建议
- 支持用户建立健康的财务习惯

对话风格：
- 专业、理性、务实
- 不带评判地理解用户的处境
- 提供清晰可行的财务规划

当用户分享财务后悔时：
1. 理解财务压力带来的焦虑
2. 帮助他们分析过去的决策
3. 制定切实可行的改善计划
4. 鼓励从小步骤开始改变'''
    },
    'leisure': {
        'model': 'doubao-seed-1-8-251228',
        'system_prompt': '''你是"生活美学导师 AI"，专注于休闲娱乐与生活品质领域。

你的角色定位：
- 帮助用户发现生活的乐趣
- 提供平衡工作与生活的方法
- 支持用户追求内心的热爱

对话风格：
- 轻松、富有创意、启发性
- 鼓励用户探索新体验
- 帮助用户找回生活的热情

当用户分享生活遗憾时：
1. 理解错过和遗憾的感受
2. 帮助他们看到当下的可能性
3. 鼓励重新拾起或发现新爱好
4. 提供具体的生活改善建议'''
    }
}


class APIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """处理POST请求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/chat':
            self.handle_chat()
        else:
            self.send_error(404, 'Not Found')

    def handle_chat(self):
        """处理对话请求"""
        try:
            # 读取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            ai_type = data.get('ai_type', 'personal-growth')
            user_message = data.get('message', '')
            conversation_history = data.get('history', [])
            
            # 获取AI配置
            persona = AI_PERSONAS.get(ai_type, AI_PERSONAS['personal-growth'])
            
            # 构建消息列表
            messages = [
                {"role": "system", "content": persona['system_prompt']}
            ]
            
            # 添加历史对话
            for msg in conversation_history:
                messages.append(msg)
            
            # 添加用户新消息
            messages.append({"role": "user", "content": user_message})
            
            # 调用火山方舟 API
            response = requests.post(
                f"{ARK_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {ARK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": persona['model'],
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # 返回成功响应
                self.send_json_response({
                    'success': True,
                    'response': ai_response,
                    'usage': result.get('usage', {})
                })
            else:
                self.send_json_response({
                    'success': False,
                    'error': f'API请求失败: {response.status_code}'
                }, 500)
                
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)

    def send_json_response(self, data, status_code=200):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"[API Server] {format % args}")


def run_server(port=None):
    """启动API服务器"""
    # Heroku使用环境变量PORT，本地使用默认8080
    if port is None:
        port = int(os.environ.get('PORT', 8080))
    
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f"\n{'='*50}")
    print(f"火山方舟 API 服务器已启动")
    print(f"监听端口: {port}")
    print(f"API地址: http://0.0.0.0:{port}/api/chat")
    print(f"{'='*50}\n")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
