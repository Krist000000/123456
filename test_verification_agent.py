#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息验证智能体 - 单元测试

测试验证智能体的核心功能
"""

import unittest
from verification_agent import VerificationAgent, VerificationResult


class TestVerificationAgent(unittest.TestCase):
    """测试验证智能体"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = VerificationAgent()
    
    def test_agent_initialization(self):
        """测试智能体初始化"""
        self.assertEqual(self.agent.name, "信息验证智能体")
        self.assertEqual(self.agent.version, "1.0.0")
    
    def test_verify_simple_claim(self):
        """测试简单信息验证"""
        claim = "中国是世界第二大经济体"
        result = self.agent.verify_information(claim)
        
        # 验证返回的结果类型
        self.assertIsInstance(result, VerificationResult)
        
        # 验证必要字段存在
        self.assertEqual(result.claim, claim)
        self.assertIsNotNone(result.conclusion)
        self.assertIsNotNone(result.confidence)
        self.assertIsInstance(result.evidence, list)
        self.assertIsInstance(result.sources, list)
        self.assertIsNotNone(result.verification_details)
        self.assertIsNotNone(result.timestamp)
    
    def test_analyze_claim(self):
        """测试信息分析功能"""
        # 测试包含时间的信息
        claim_with_time = "立陶宛在2021年允许台湾设立代表处"
        analysis = self.agent._analyze_claim(claim_with_time)
        self.assertIn('时间信息', analysis['key_points'])
        
        # 测试包含地点的信息
        claim_with_location = "中国国家位于亚洲东部"
        analysis = self.agent._analyze_claim(claim_with_location)
        self.assertIn('地点信息', analysis['key_points'])
        
        # 测试包含数据的信息
        claim_with_data = "中国人口超过14亿"
        analysis = self.agent._analyze_claim(claim_with_data)
        self.assertIn('数据信息', analysis['key_points'])
    
    def test_web_search(self):
        """测试网络搜索功能"""
        claim = "测试信息"
        analysis = {'key_points': ['测试'], 'claim_type': '测试'}
        search_results = self.agent._web_search(claim, analysis)
        
        # 验证返回结果
        self.assertIsInstance(search_results, list)
        self.assertGreater(len(search_results), 0)
        
        # 验证结果包含必要字段
        for result in search_results:
            self.assertIn('title', result)
            self.assertIn('url', result)
            self.assertIn('relevance', result)
    
    def test_collect_authoritative_sources(self):
        """测试权威来源收集"""
        search_results = [
            {
                'title': '测试来源1',
                'url': 'https://example.com/1',
                'snippet': '测试内容1',
                'relevance': '高',
                'source_type': 'official'
            },
            {
                'title': '测试来源2',
                'url': 'https://example.com/2',
                'snippet': '测试内容2',
                'relevance': '中',
                'source_type': 'academic'
            }
        ]
        
        sources = self.agent._collect_authoritative_sources(search_results)
        
        # 验证来源数量
        self.assertEqual(len(sources), 2)
        
        # 验证来源按相关度排序
        self.assertEqual(sources[0].relevance, '高')
    
    def test_conclusion_generation(self):
        """测试结论生成"""
        # 测试高一致性分数
        high_score_result = {
            'evidence': ['证据1', '证据2'],
            'details': '详细信息',
            'consistency_score': 0.9
        }
        conclusion = self.agent._generate_conclusion(high_score_result)
        self.assertEqual(conclusion['conclusion'], '真实')
        self.assertEqual(conclusion['confidence'], '高')
        
        # 测试中等一致性分数
        medium_score_result = {
            'evidence': ['证据1'],
            'details': '详细信息',
            'consistency_score': 0.6
        }
        conclusion = self.agent._generate_conclusion(medium_score_result)
        self.assertEqual(conclusion['conclusion'], '部分真实')
        
        # 测试低一致性分数
        low_score_result = {
            'evidence': [],
            'details': '详细信息',
            'consistency_score': 0.1
        }
        conclusion = self.agent._generate_conclusion(low_score_result)
        self.assertEqual(conclusion['conclusion'], '无法充分验证')


class TestVerificationResult(unittest.TestCase):
    """测试验证结果数据结构"""
    
    def test_verification_result_structure(self):
        """测试验证结果数据结构"""
        from dataclasses import asdict
        from verification_agent import VerificationSource
        
        source = VerificationSource(
            title="测试来源",
            url="https://example.com",
            relevance="高",
            key_points=["要点1"]
        )
        
        result = VerificationResult(
            claim="测试信息",
            conclusion="真实",
            confidence="高",
            evidence=["证据1", "证据2"],
            sources=[source],
            verification_details="测试详情",
            timestamp="2026-02-13 13:30:00"
        )
        
        # 验证可以转换为字典
        result_dict = asdict(result)
        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict['claim'], "测试信息")
        self.assertEqual(result_dict['conclusion'], "真实")


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
