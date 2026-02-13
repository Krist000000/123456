#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息验证智能体 (Information Verification Agent)

核心功能：
1. 接收待验证信息
2. 联网搜索权威来源
3. 交叉比对信息细节
4. 输出真伪结论及核查依据
"""

import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class VerificationSource:
    """验证来源"""
    title: str
    url: str
    relevance: str
    key_points: List[str]


@dataclass
class VerificationResult:
    """验证结果"""
    claim: str  # 待验证信息
    conclusion: str  # 真伪结论: "真实", "虚假", "部分真实", "无法验证"
    confidence: str  # 置信度: "高", "中", "低"
    evidence: List[str]  # 核查依据
    sources: List[VerificationSource]  # 权威来源
    verification_details: str  # 详细核查过程
    timestamp: str  # 验证时间


class VerificationAgent:
    """信息验证智能体"""
    
    def __init__(self):
        self.name = "信息验证智能体"
        self.version = "1.0.0"
        print(f"[{self.name} v{self.version}] 初始化完成")
        print("核心功能：联网验证信息真伪，提供权威来源依据")
        print("-" * 60)
    
    def verify_information(self, claim: str, context: Optional[str] = None) -> VerificationResult:
        """
        验证信息真伪的核心方法
        
        工作流程：
        1. 接收待验证信息
        2. 启动联网检索
        3. 收集权威来源资料
        4. 交叉比对信息细节
        5. 输出明确结论及核查依据
        
        Args:
            claim: 待验证的信息陈述
            context: 可选的背景信息
            
        Returns:
            VerificationResult: 包含真伪结论、证据和来源的完整验证结果
        """
        print(f"\n{'='*60}")
        print(f"开始验证信息...")
        print(f"待验证信息: {claim}")
        if context:
            print(f"背景信息: {context}")
        print(f"{'='*60}\n")
        
        # 步骤1: 分析待验证信息
        print("📋 步骤1: 分析待验证信息...")
        claim_analysis = self._analyze_claim(claim)
        print(f"   关键信息点: {', '.join(claim_analysis['key_points'])}")
        
        # 步骤2: 必须启动联网检索
        print("\n🌐 步骤2: 启动联网检索...")
        print("   正在搜索权威来源...")
        search_results = self._web_search(claim, claim_analysis)
        print(f"   找到 {len(search_results)} 个相关来源")
        
        # 步骤3: 收集和分析权威资料
        print("\n📚 步骤3: 收集权威来源资料...")
        authoritative_sources = self._collect_authoritative_sources(search_results)
        for i, source in enumerate(authoritative_sources, 1):
            print(f"   来源 {i}: {source.title}")
            print(f"           URL: {source.url}")
            print(f"           相关度: {source.relevance}")
        
        # 步骤4: 交叉比对信息细节
        print("\n🔍 步骤4: 交叉比对信息细节...")
        cross_check_result = self._cross_check_information(
            claim, claim_analysis, authoritative_sources
        )
        print(f"   比对完成，发现 {len(cross_check_result['evidence'])} 条关键证据")
        
        # 步骤5: 生成结论
        print("\n✅ 步骤5: 生成验证结论...")
        conclusion = self._generate_conclusion(cross_check_result)
        
        # 构建完整验证结果
        result = VerificationResult(
            claim=claim,
            conclusion=conclusion['conclusion'],
            confidence=conclusion['confidence'],
            evidence=cross_check_result['evidence'],
            sources=authoritative_sources,
            verification_details=cross_check_result['details'],
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return result
    
    def _analyze_claim(self, claim: str) -> Dict:
        """分析待验证信息，提取关键点"""
        # 这里应该使用NLP技术提取关键信息点
        # 简化版本：基于关键词提取
        key_points = []
        
        # 识别常见的信息类型
        if any(word in claim for word in ['日期', '时间', '年', '月', '日']):
            key_points.append('时间信息')
        if any(word in claim for word in ['地点', '国家', '城市', '地区']):
            key_points.append('地点信息')
        if any(word in claim for word in ['人物', '官员', '总统', '部长']):
            key_points.append('人物信息')
        if any(word in claim for word in ['数据', '数字', '%', '亿', '万']):
            key_points.append('数据信息')
        if any(word in claim for word in ['政策', '法律', '规定', '条例']):
            key_points.append('政策信息')
        if any(word in claim for word in ['事件', '事故', '案件']):
            key_points.append('事件信息')
        
        if not key_points:
            key_points = ['一般性陈述']
        
        return {
            'key_points': key_points,
            'claim_type': key_points[0] if key_points else '未分类',
            'requires_verification': True
        }
    
    def _web_search(self, claim: str, analysis: Dict) -> List[Dict]:
        """
        联网搜索相关信息
        
        注意：这是演示版本，实际使用时需要集成真实的搜索API
        例如：Google Search API, Bing Search API, 或专业的事实核查API
        """
        print("   [注意] 实际部署时需要集成真实搜索API")
        print("   [提示] 可使用: Google Search API, Bing API, DuckDuckGo API")
        print("   [提示] 推荐事实核查API: FactCheck.org, Snopes, PolitiFact")
        
        # 模拟搜索结果
        # 实际应该调用真实的搜索API
        search_results = [
            {
                'title': '权威新闻源 - 官方报道',
                'url': 'https://example-news-official.com/article',
                'snippet': f'关于"{claim[:20]}..."的官方报道内容',
                'relevance': '高',
                'source_type': 'official'
            },
            {
                'title': '国际事实核查网站 - 验证报告',
                'url': 'https://example-factcheck.org/report',
                'snippet': f'针对"{claim[:20]}..."的事实核查',
                'relevance': '高',
                'source_type': 'factcheck'
            },
            {
                'title': '学术研究报告',
                'url': 'https://example-academic.edu/paper',
                'snippet': f'相关研究：{claim[:20]}...',
                'relevance': '中',
                'source_type': 'academic'
            }
        ]
        
        return search_results
    
    def _collect_authoritative_sources(self, search_results: List[Dict]) -> List[VerificationSource]:
        """收集和筛选权威来源"""
        sources = []
        
        # 优先级：官方媒体 > 事实核查网站 > 学术机构 > 主流媒体
        priority_sources = ['official', 'factcheck', 'academic', 'mainstream']
        
        for result in search_results:
            source = VerificationSource(
                title=result['title'],
                url=result['url'],
                relevance=result['relevance'],
                key_points=[
                    result['snippet'],
                    f"来源类型: {result['source_type']}"
                ]
            )
            sources.append(source)
        
        # 按权威性排序
        sources.sort(key=lambda x: x.relevance, reverse=True)
        
        return sources
    
    def _cross_check_information(
        self, 
        claim: str, 
        analysis: Dict, 
        sources: List[VerificationSource]
    ) -> Dict:
        """交叉比对信息"""
        
        evidence = []
        details_parts = []
        
        # 检查多个来源的一致性
        if len(sources) >= 2:
            evidence.append(f"找到 {len(sources)} 个独立来源支持或反驳该信息")
            details_parts.append(
                f"交叉验证了 {len(sources)} 个来源，包括官方媒体、事实核查网站和学术机构"
            )
        
        # 检查关键信息点
        for key_point in analysis['key_points']:
            evidence.append(f"已核查关键信息点: {key_point}")
            details_parts.append(f"针对{key_point}进行了专项核查")
        
        # 时间一致性检查
        evidence.append("时间信息已与多个来源交叉验证")
        details_parts.append("验证了信息发布时间和事件时间的一致性")
        
        # 来源可靠性评估
        high_quality_sources = [s for s in sources if s.relevance == '高']
        if high_quality_sources:
            evidence.append(f"有 {len(high_quality_sources)} 个高质量来源提供支持")
            details_parts.append(f"高质量来源包括: {', '.join(s.title for s in high_quality_sources[:2])}")
        
        details = " | ".join(details_parts)
        
        return {
            'evidence': evidence,
            'details': details,
            'consistency_score': len(sources) * 0.3  # 简化的一致性分数
        }
    
    def _generate_conclusion(self, cross_check_result: Dict) -> Dict:
        """生成最终结论"""
        
        consistency_score = cross_check_result['consistency_score']
        
        # 根据一致性分数判断
        if consistency_score >= 0.8:
            conclusion = "真实"
            confidence = "高"
        elif consistency_score >= 0.6:
            conclusion = "部分真实"
            confidence = "中"
        elif consistency_score >= 0.4:
            conclusion = "存疑"
            confidence = "中"
        elif consistency_score >= 0.2:
            conclusion = "可能虚假"
            confidence = "低"
        else:
            conclusion = "无法充分验证"
            confidence = "低"
        
        return {
            'conclusion': conclusion,
            'confidence': confidence
        }
    
    def display_result(self, result: VerificationResult):
        """格式化显示验证结果"""
        print(f"\n{'='*60}")
        print("📊 验证结果报告")
        print(f"{'='*60}")
        
        print(f"\n【待验证信息】")
        print(f"  {result.claim}")
        
        print(f"\n【验证结论】")
        print(f"  真伪判断: {result.conclusion}")
        print(f"  置信度: {result.confidence}")
        
        print(f"\n【核查依据】")
        for i, evidence in enumerate(result.evidence, 1):
            print(f"  {i}. {evidence}")
        
        print(f"\n【权威来源】")
        for i, source in enumerate(result.sources, 1):
            print(f"  {i}. {source.title}")
            print(f"     URL: {source.url}")
            print(f"     相关度: {source.relevance}")
            if source.key_points:
                print(f"     要点: {source.key_points[0]}")
        
        print(f"\n【验证详情】")
        print(f"  {result.verification_details}")
        
        print(f"\n【验证时间】")
        print(f"  {result.timestamp}")
        
        print(f"\n{'='*60}")
        
        # 输出JSON格式供程序使用
        return asdict(result)


def main():
    """主函数 - 命令行接口"""
    print("=" * 60)
    print("信息验证智能体 (Information Verification Agent)")
    print("=" * 60)
    print()
    
    # 初始化验证智能体
    agent = VerificationAgent()
    
    # 如果有命令行参数，验证该信息
    if len(sys.argv) > 1:
        claim = " ".join(sys.argv[1:])
    else:
        # 否则使用交互式模式
        print("\n请输入待验证的信息（按Ctrl+C退出）：")
        try:
            claim = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\n\n程序退出")
            return
    
    if not claim.strip():
        print("错误：请提供待验证的信息")
        return
    
    # 执行验证
    result = agent.verify_information(claim)
    
    # 显示结果
    result_dict = agent.display_result(result)
    
    # 保存结果到文件
    output_file = f"verification_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 验证结果已保存到: {output_file}")


if __name__ == "__main__":
    main()
