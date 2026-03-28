#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息验证智能体 - 示例用法

演示如何使用验证智能体进行信息真伪验证
"""

from verification_agent import VerificationAgent


def example_1():
    """示例1: 验证简单事实性陈述"""
    print("\n" + "="*60)
    print("示例1: 验证简单事实性陈述")
    print("="*60)
    
    agent = VerificationAgent()
    result = agent.verify_information("中国是世界第二大经济体")
    agent.display_result(result)


def example_2():
    """示例2: 验证包含时间和地点的事件"""
    print("\n" + "="*60)
    print("示例2: 验证包含时间和地点的事件")
    print("="*60)
    
    agent = VerificationAgent()
    result = agent.verify_information("立陶宛在2021年允许台湾设立代表处")
    agent.display_result(result)


def example_3():
    """示例3: 验证带有数据的陈述"""
    print("\n" + "="*60)
    print("示例3: 验证带有数据的陈述")
    print("="*60)
    
    agent = VerificationAgent()
    result = agent.verify_information("中国人口超过14亿")
    agent.display_result(result)


def example_4():
    """示例4: 验证政策性陈述"""
    print("\n" + "="*60)
    print("示例4: 验证政策性陈述")
    print("="*60)
    
    agent = VerificationAgent()
    result = agent.verify_information(
        "美国在2022年通过了芯片法案限制对华出口"
    )
    agent.display_result(result)


def example_5():
    """示例5: 验证国际事件"""
    print("\n" + "="*60)
    print("示例5: 验证国际事件")
    print("="*60)
    
    agent = VerificationAgent()
    result = agent.verify_information("2024年巴黎举办奥运会")
    agent.display_result(result)


def main():
    """运行所有示例"""
    print("="*60)
    print("信息验证智能体 - 使用示例集合")
    print("="*60)
    print("\n本脚本演示验证智能体的各种使用场景")
    print("包括：事实、事件、数据、政策等不同类型的信息验证\n")
    
    examples = [
        ("验证简单事实", example_1),
        ("验证历史事件", example_2),
        ("验证数据陈述", example_3),
        ("验证政策信息", example_4),
        ("验证国际事件", example_5),
    ]
    
    print("可用示例：")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\n选择要运行的示例（输入序号，或按回车运行所有示例）：")
    try:
        choice = input("> ").strip()
        
        if not choice:
            # 运行所有示例
            for name, func in examples:
                func()
                input("\n按回车继续下一个示例...")
        else:
            # 运行选定的示例
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                examples[idx][1]()
            else:
                print("无效的选择")
    
    except (ValueError, KeyboardInterrupt):
        print("\n程序退出")


if __name__ == "__main__":
    main()
