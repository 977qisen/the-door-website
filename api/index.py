from http.server import BaseHTTPRequestHandler
import json
import os

# 从环境变量获取API密钥
ARK_API_KEY = os.environ.get('ARK_API_KEY', '')

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            message = data.get('message', '')
            ai_type = data.get('ai_type', 'personal-growth')
            
            # 模拟AI回复（实际使用时可以接入真实API）
            responses = {
                'personal-growth': [
                    "我理解你的感受。每个人都会在成长路上遇到迷茫，重要的是我们如何面对这些挑战。",
                    "感谢你愿意分享这些。这种反思本身就是一种勇气，让我们一起探索如何更好地前进。",
                    "我能感受到你的情绪。过去的经历虽然无法改变，但我们可以改变对它们的看法。"
                ],
                'career': [
                    "职业发展中的选择确实很重要。让我们一起分析你的情况，找到最适合的方向。",
                    "每一个职业决定都是一次学习的机会。重要的是从中吸取经验，继续前进。",
                    "职业生涯是马拉松，不是短跑。现在调整方向完全来得及。"
                ],
                'health': [
                    "健康是人生最宝贵的财富。让我们一起制定一个适合你的健康计划。",
                    "改变生活习惯需要时间和耐心。从小目标开始，一步步来。",
                    "你的身体会感谢你现在做出的每一个健康选择。"
                ],
                'family': [
                    "家庭关系需要用心经营。沟通是解决问题的关键。",
                    "家人之间的误解往往源于缺乏沟通。试着换位思考，理解对方的立场。",
                    "修复关系需要勇气，但这一切都是值得的。"
                ],
                'social': [
                    "人际关系是人生的重要组成部分。让我们一起提升你的社交能力。",
                    "真诚的交流是建立良好关系的基础。做真实的自己就好。",
                    "社交技能是可以学习的。每一次互动都是练习的机会。"
                ],
                'finance': [
                    "理财是一项重要的生活技能。让我们一起学习如何更好地管理财务。",
                    "每一个财务决定都会影响未来。理性分析，谨慎决策。",
                    "积少成多，理财从点滴开始。"
                ],
                'leisure': [
                    "生活需要平衡，娱乐和放松同样重要。",
                    "找到让自己快乐的事情，这是生活的意义之一。",
                    "适当的放松能让你更好地面对工作和生活的挑战。"
                ]
            }
            
            # 根据关键词匹配更具体的回复
            if '梦想' in message:
                response = "梦想是人生的指南针。虽然现在可能没有坚持当初的梦想，但这并不意味着你不能重新追寻。重要的是现在开始行动。"
            elif '时间' in message or '浪费' in message:
                response = "时间确实宝贵，但所谓的'浪费'也是一种经历。每一段经历都让你成为了现在的你。重要的是从现在开始，让每一刻都有意义。"
            elif '机会' in message or '错过' in message:
                response = "错过的机会确实让人遗憾，但人生还有很多机会等待着你。保持开放的心态，新的机会可能就在下一个转角。"
            elif '改变' in message or '开始' in message:
                response = "改变从来都不会太晚。重要的是迈出第一步。让我们一起制定一个可行的计划，一步步朝着目标前进。"
            elif message in ['持续后悔中', '不再后悔了']:
                if message == '持续后悔中':
                    response = "我理解你的感受。后悔是一种正常的情绪，它说明你对自己的人生有所期待。让我们继续聊聊，看看如何把这些遗憾转化为成长的动力。"
                else:
                    response = "很高兴听到你开始接纳过去的自己。记住，每一个选择都塑造了今天的你，而今天的你正在创造更好的明天。"
            else:
                # 随机选择对应类型的回复
                type_responses = responses.get(ai_type, responses['personal-growth'])
                import random
                response = random.choice(type_responses)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                'success': True,
                'response': response
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'ok',
            'message': 'API is running'
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
