#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八卦象数疗法 - 命令行版
数据来源: xiangshu_data.py
"""

import sys
import os

try:
    from xiangshu_data import RECIPES
except ImportError:
    print("错误：无法导入 xiangshu_data.py，请确保该文件在同一目录下。")
    sys.exit(1)


def search_symptoms(keyword):
    """搜索症状关键词，返回匹配配方"""
    results = []
    kw = keyword.strip().lower()
    for r in RECIPES:
        for s in r["symptoms"]:
            if kw in s.lower():
                results.append(r)
                break
    return results


def main():
    sym_count = len(set(s for r in RECIPES for s in r["symptoms"]))
    print("=" * 60)
    print("  八卦象数疗法查询系统")
    print("  共 {} 条配方，{} 个症状关键词".format(len(RECIPES), sym_count))
    print("=" * 60)
    print()
    print("输入症状关键词进行搜索，输入 q 退出")
    print("支持的症状关键词示例：头痛、感冒、咳嗽、失眠、腰痛...")
    print()

    while True:
        try:
            kw = input("请输入症状关键词: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n退出。")
            break
        if not kw:
            continue
        if kw.lower() in ("q", "quit", "exit"):
            print("再见！")
            break

        results = search_symptoms(kw)
        if not results:
            print("未找到与「{}」相关的配方，请尝试其他关键词。\n".format(kw))
            continue

        print("\n找到 {} 条相关配方：".format(len(results)))
        print("-" * 60)
        for i, r in enumerate(results, 1):
            syms = "、".join(r["symptoms"])
            print("{}. 症状: {}".format(i, syms))
            print("   象数: {}".format(r["formula"]))
            print("   方义: {}".format(r["explanation"]))
            print()
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
