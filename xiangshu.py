# -*- coding: utf-8 -*-
"""
八卦象数疗法交互式查询程序 - Bilingual Launcher (Chinese / English)
使用方法 / Usage: python xiangshu.py
"""
import sys

def main():
    print("\n" + "=" * 50)
    print("  Eight Diagrams Numerology Therapy")
    print("  八卦象数疗法交互式查询程序")
    print("=" * 50)
    print("\n  [1] 中文版 (Chinese)")
    print("  [2] English version")
    print()

    while True:
        choice = input("Select / 选择 (1 or 2): ").strip()
        if choice == '1':
            import xiangshu_gui
            xiangshu_gui.main()
            break
        elif choice == '2':
            import xiangshu_data_en
            import xiangshu_gui
            xiangshu_gui.DATA = xiangshu_data_en.RECIPES
            xiangshu_gui.ALL_SYMPTOMS = sorted(set(
                s for r in xiangshu_data_en.RECIPES
                for s in r['symptoms']
            ))
            xiangshu_gui.main()
            break
        else:
            print("Invalid input / 无效输入，请输入 1 或 2")

if __name__ == '__main__':
    main()
