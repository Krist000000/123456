#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息验证智能体 - Web API接口

提供HTTP API接口供前端调用
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from verification_agent import VerificationAgent
from dataclasses import asdict
import json

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化验证智能体
agent = VerificationAgent()

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>信息验证智能体 - Information Verification Agent</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", 
                         "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.2em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 5px;
        }
        
        .info-box h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .info-box ul {
            margin-left: 20px;
            color: #555;
        }
        
        .info-box li {
            margin: 5px 0;
        }
        
        .input-section {
            margin-bottom: 30px;
        }
        
        .input-section label {
            display: block;
            font-size: 1.1em;
            color: #333;
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .input-section textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            min-height: 100px;
            transition: border-color 0.3s;
        }
        
        .input-section textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: 600;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .button:active {
            transform: translateY(0);
        }
        
        .button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .loading.active {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result {
            display: none;
            margin-top: 30px;
            padding: 25px;
            border-radius: 8px;
            background: #f8f9fa;
        }
        
        .result.active {
            display: block;
        }
        
        .result h2 {
            color: #333;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .result-item {
            margin: 20px 0;
        }
        
        .result-item h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .conclusion {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 1.1em;
        }
        
        .conclusion.真实 {
            background: #d4edda;
            color: #155724;
        }
        
        .conclusion.虚假 {
            background: #f8d7da;
            color: #721c24;
        }
        
        .conclusion.部分真实 {
            background: #fff3cd;
            color: #856404;
        }
        
        .conclusion.存疑,
        .conclusion.可能虚假,
        .conclusion.无法充分验证 {
            background: #e2e3e5;
            color: #383d41;
        }
        
        .confidence {
            margin-left: 10px;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9em;
        }
        
        .confidence.高 {
            background: #28a745;
            color: white;
        }
        
        .confidence.中 {
            background: #ffc107;
            color: #333;
        }
        
        .confidence.低 {
            background: #dc3545;
            color: white;
        }
        
        .evidence-list {
            list-style: none;
            padding: 0;
        }
        
        .evidence-list li {
            padding: 10px;
            margin: 8px 0;
            background: white;
            border-left: 3px solid #667eea;
            border-radius: 3px;
        }
        
        .source-card {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
        }
        
        .source-card h4 {
            color: #333;
            margin-bottom: 8px;
        }
        
        .source-card a {
            color: #667eea;
            text-decoration: none;
            word-break: break-all;
        }
        
        .source-card a:hover {
            text-decoration: underline;
        }
        
        .source-relevance {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 0.85em;
            margin-left: 10px;
        }
        
        .source-relevance.高 {
            background: #d4edda;
            color: #155724;
        }
        
        .source-relevance.中 {
            background: #fff3cd;
            color: #856404;
        }
        
        .source-relevance.低 {
            background: #f8d7da;
            color: #721c24;
        }
        
        .timestamp {
            text-align: center;
            color: #999;
            font-size: 0.9em;
            margin-top: 20px;
        }
        
        .example-buttons {
            margin: 20px 0;
        }
        
        .example-btn {
            display: inline-block;
            margin: 5px;
            padding: 8px 15px;
            background: #e9ecef;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background 0.2s;
        }
        
        .example-btn:hover {
            background: #dee2e6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 信息验证智能体</h1>
            <p>Information Verification Agent - 帮您验证信息真伪</p>
        </div>
        
        <div class="content">
            <div class="info-box">
                <h3>📋 核心功能</h3>
                <ul>
                    <li><strong>联网验证：</strong>自动搜索权威来源，核查信息真伪</li>
                    <li><strong>交叉比对：</strong>对比多个来源，确保信息准确性</li>
                    <li><strong>详细报告：</strong>提供完整的验证依据和来源链接</li>
                    <li><strong>可信评级：</strong>标注信息可信度和验证置信度</li>
                </ul>
            </div>
            
            <div class="input-section">
                <label for="claim">请输入需要验证的信息：</label>
                <textarea id="claim" placeholder="例如：立陶宛在2021年允许台湾设立代表处"></textarea>
                
                <div class="example-buttons">
                    <strong>示例：</strong>
                    <span class="example-btn" onclick="fillExample('立陶宛在2021年允许台湾设立代表处')">立陶宛台湾代表处</span>
                    <span class="example-btn" onclick="fillExample('中国是世界第二大经济体')">中国经济规模</span>
                    <span class="example-btn" onclick="fillExample('2024年巴黎举办奥运会')">巴黎奥运会</span>
                </div>
            </div>
            
            <button class="button" onclick="verifyInformation()">🔍 开始验证</button>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在联网搜索验证...</p>
            </div>
            
            <div class="result" id="result">
                <h2>📊 验证结果</h2>
                
                <div class="result-item">
                    <h3>待验证信息</h3>
                    <p id="result-claim"></p>
                </div>
                
                <div class="result-item">
                    <h3>验证结论</h3>
                    <div>
                        <span class="conclusion" id="result-conclusion"></span>
                        <span class="confidence" id="result-confidence"></span>
                    </div>
                </div>
                
                <div class="result-item">
                    <h3>核查依据</h3>
                    <ul class="evidence-list" id="result-evidence"></ul>
                </div>
                
                <div class="result-item">
                    <h3>权威来源</h3>
                    <div id="result-sources"></div>
                </div>
                
                <div class="result-item">
                    <h3>验证详情</h3>
                    <p id="result-details"></p>
                </div>
                
                <div class="timestamp" id="result-timestamp"></div>
            </div>
        </div>
    </div>
    
    <script>
        function fillExample(text) {
            document.getElementById('claim').value = text;
        }
        
        async function verifyInformation() {
            const claim = document.getElementById('claim').value.trim();
            
            if (!claim) {
                alert('请输入需要验证的信息');
                return;
            }
            
            // 显示加载状态
            document.getElementById('loading').classList.add('active');
            document.getElementById('result').classList.remove('active');
            document.querySelector('.button').disabled = true;
            
            try {
                const response = await fetch('/api/verify', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ claim: claim })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    displayResult(data.result);
                } else {
                    alert('验证失败: ' + data.error);
                }
            } catch (error) {
                alert('请求失败: ' + error.message);
            } finally {
                document.getElementById('loading').classList.remove('active');
                document.querySelector('.button').disabled = false;
            }
        }
        
        function displayResult(result) {
            // 显示待验证信息
            document.getElementById('result-claim').textContent = result.claim;
            
            // 显示结论
            const conclusionElem = document.getElementById('result-conclusion');
            conclusionElem.textContent = result.conclusion;
            conclusionElem.className = 'conclusion ' + result.conclusion;
            
            // 显示置信度
            const confidenceElem = document.getElementById('result-confidence');
            confidenceElem.textContent = '置信度: ' + result.confidence;
            confidenceElem.className = 'confidence ' + result.confidence;
            
            // 显示证据
            const evidenceList = document.getElementById('result-evidence');
            evidenceList.innerHTML = '';
            result.evidence.forEach(evidence => {
                const li = document.createElement('li');
                li.textContent = evidence;
                evidenceList.appendChild(li);
            });
            
            // 显示来源
            const sourcesDiv = document.getElementById('result-sources');
            sourcesDiv.innerHTML = '';
            result.sources.forEach(source => {
                const card = document.createElement('div');
                card.className = 'source-card';
                card.innerHTML = `
                    <h4>
                        ${source.title}
                        <span class="source-relevance ${source.relevance}">相关度: ${source.relevance}</span>
                    </h4>
                    <p><a href="${source.url}" target="_blank">${source.url}</a></p>
                    ${source.key_points.length > 0 ? '<p>' + source.key_points[0] + '</p>' : ''}
                `;
                sourcesDiv.appendChild(card);
            });
            
            // 显示详情
            document.getElementById('result-details').textContent = result.verification_details;
            
            // 显示时间戳
            document.getElementById('result-timestamp').textContent = '验证时间: ' + result.timestamp;
            
            // 显示结果区域
            document.getElementById('result').classList.add('active');
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/verify', methods=['POST'])
def verify():
    """验证API接口"""
    try:
        data = request.get_json()
        claim = data.get('claim', '').strip()
        context = data.get('context', None)
        
        if not claim:
            return jsonify({
                'success': False,
                'error': '请提供待验证的信息'
            }), 400
        
        # 执行验证
        result = agent.verify_information(claim, context)
        
        # 转换为字典格式
        result_dict = asdict(result)
        
        return jsonify({
            'success': True,
            'result': result_dict
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'agent': agent.name,
        'version': agent.version
    })


if __name__ == '__main__':
    print("=" * 60)
    print("启动信息验证智能体 Web 服务")
    print("=" * 60)
    print(f"访问地址: http://localhost:5000")
    print(f"API接口: http://localhost:5000/api/verify")
    print(f"健康检查: http://localhost:5000/api/health")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
