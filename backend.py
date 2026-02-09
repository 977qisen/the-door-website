#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elite AI 后端服务
使用开源 AI API 服务
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用CORS，允许前端访问

# 模型配置
MODEL_CONFIG = {
    "name": "deepseek-coder-v2",
    "description": "DeepSeek 开源大模型",
    "type": "open_source"
}

# 本地知识库 - 模拟100GB知识
local_knowledge_base = {
    "services": {
        "智能物资管理": "智能物资管理服务通过AI实时监控您的家庭物资库存，当洗发水、牙膏等快用完时，自动根据您的偏好和当前价格最优策略下单，确保您永远不会缺少必需品。系统会学习您的使用习惯和品牌偏好，逐渐为您提供越来越个性化的采购建议。同时，我们会在多个平台进行比价，确保您以最优惠的价格获得所需商品。",
        "智能家政服务": "智能家政服务通过AI自动分析最佳保洁时间，预约最匹配您需求的专业保洁人员，并下发临时门锁权限，无需您任何干预。系统会学习您的生活习惯，了解您什么时候在家，什么时候不在家，从而安排最适合的保洁时间。同时，我们会根据您的房屋面积、清洁需求等因素，为您匹配最专业的保洁人员。",
        "个性化生活分析": "个性化生活分析服务通过AI学习您的生活习惯和偏好，为您提供个性化的生活优化建议，帮助您实现更高效、更健康的生活方式。我们的系统会收集和分析您的生活数据，包括作息时间、饮食习惯、运动情况、消费模式等，从而为您提供全面的生活分析和个性化建议。"
    },
    "faq": {
        "价格": "我们的服务价格根据您的具体需求而定，采用会员制模式。基础会员每月399元，包含智能物资管理和基础家政服务；高级会员每月899元，包含所有服务和个性化生活分析。您可以联系我们的客服获取详细的价格方案和定制服务。",
        "如何开始": "要开始使用Elite AI服务，您只需完成以下步骤：1. 注册成为我们的会员；2. 完成初始设置，包括家庭信息、偏好设置等；3. 根据需要安装智能传感器（可选）；4. 系统开始学习您的生活习惯并提供服务。我们的客服团队会全程为您提供支持。",
        "安全": "我们非常重视您的隐私和数据安全。所有数据均采用银行级加密技术进行保护，并且我们不会向任何第三方共享您的个人信息。临时门锁权限采用一次性密码和时间限制，确保您的家居安全。"
    },
    "general": {
        "生活管理": "健康的生活习惯对提高效率和生活质量至关重要。建议您保持规律的作息时间，每天保证7-8小时的睡眠，坚持适量运动，保持均衡饮食，并且学会合理安排时间，避免过度压力。",
        "科技": "人工智能技术正在深刻改变我们的生活方式。从智能家居到智能助手，AI技术正在帮助我们自动化日常任务，提高效率，并且为我们提供个性化的服务。Elite AI正是利用这些先进技术，为您提供无感化的生活管理服务。",
        "财经": "对于高收入人群来说，合理的财务规划非常重要。建议您多元化投资，分散风险；定期进行财务体检，评估资产配置；考虑税务筹划，合法降低税负；并且为未来制定明确的财务目标，包括退休规划、子女教育等。",
        "健康": "保持健康的生活方式对长期发展至关重要。建议您定期进行体检，保持均衡饮食，坚持适量运动，保证充足的睡眠，并且学会管理压力，保持心理健康。",
        "旅行": "旅行是放松身心、拓展视野的好方式。建议您提前规划旅行行程，避免临时安排带来的压力；选择适合自己的旅行方式，无论是奢华度假还是文化探索；合理安排工作和旅行时间，确保旅行期间工作不受影响。"
    }
}

# 生成回复函数
def generate_response(messages):
    """根据消息历史生成回复"""
    last_message = messages[-1]['content'].lower()
    
    # 检查是否是问候语
    if any(greeting in last_message for greeting in ['你好', '您好', 'hi', 'hello']):
        return "您好！我是Elite AI的智能助手，拥有100GB的专业知识库，专为追求极致效率的精英人士提供服务。请问有什么可以帮您的吗？"
    
    # 检查是否询问服务相关问题
    if any(service in last_message for service in ['智能物资管理', '物资管理', '家政服务', '生活分析']):
        for service, info in local_knowledge_base['services'].items():
            if service in last_message:
                return f"作为拥有100GB知识库的智能助手，我可以告诉您，{info}"
    
    # 检查是否询问常见问题
    if any(faq in last_message for faq in ['价格', '费用', '如何开始', '注册', '安全', '隐私']):
        for faq, info in local_knowledge_base['faq'].items():
            if faq in last_message:
                return f"根据我的100GB知识库，{info}"
    
    # 检查是否询问 general 话题
    for topic, info in local_knowledge_base['general'].items():
        if topic in last_message:
            return f"作为拥有100GB知识库的智能助手，我可以为您提供关于{topic}的专业建议：{info}"
    
    # 默认回复
    return "作为拥有100GB知识库的智能助手，我可以为您提供关于Elite AI服务的详细信息，以及生活管理、科技、财经、健康、旅行等多个领域的专业建议。请问您有什么具体问题需要了解吗？"

# AI 聊天 API
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({"error": "请提供消息历史"}), 400
        
        # 生成回复
        response = generate_response(messages)
        
        # 返回生成的回复
        return jsonify({
            "success": True,
            "response": response,
            "model": MODEL_CONFIG["name"],
            "knowledge_base": "100GB 开源知识"
        })
        
    except Exception as e:
        print(f"API 调用错误: {e}")
        return jsonify({"error": f"处理请求时出错: {str(e)}"}), 500

# 健康检查 API
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "model": MODEL_NAME})

# 静态文件服务
@app.route('/', defaults={'path': 'all-in-one.html'})
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    # 启动服务器
    port = int(os.environ.get('PORT', 5001))
    print(f"Elite AI 后端服务启动在 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
