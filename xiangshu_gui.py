#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八卦象数疗法 - GUI版 (tkinter)
数据来源: xiangshu_data.py
独立运行，无需其他文件（除 xiangshu_data.py）
v2.0: 增加右侧症状清单侧边栏，输入时实时筛选，点击即搜
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import re

try:
    from xiangshu_data import RECIPES
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("错误", "无法导入 xiangshu_data.py\n请确保该文件在同一目录下。")
    raise SystemExit(1)

# 收集所有唯一症状并排序
ALL_SYMPTOMS = sorted(set(s for r in RECIPES for s in r["symptoms"]))

COMMON_SYMPTOMS = [
    "头痛", "偏头痛", "感冒", "咳嗽", "失眠", "多梦",
    "腰痛", "胃痛", "关节炎", "高血压", "糖尿病",
    "近视", "耳鸣", "鼻炎", "口腔溃疡", "牙痛",
    "湿疹", "痤疮", "痛经", "更年期", "抑郁",
    "面瘫", "帕金森", "偏瘫", "坐骨神经痛",
    "颈椎病", "肩周炎", "静脉曲张", "脱发",
    "阳痿", "遗精", "前列腺炎", "肾结石",
    "肥胖", "戒烟", "解酒", "晕车", "美白",
]

BASIC_KNOWLEDGE = (
    "八卦象数疗法基础知识\n"
    "=" * 50 + "\n\n"
    "八卦象数疗法是李山玉创立的一种自然疗法，\n"
    "通过默念或贴敷特定数字组合（象数）来调理身体。\n\n"
    "八卦对应数字：\n"
    "  1 - 乾卦 - 头、脑、督脉、大肠\n"
    "  2 - 兑卦 - 肺、鼻、咽喉、皮肤\n"
    "  3 - 离卦 - 心、目、血、舌\n"
    "  4 - 震卦 - 肝、胆、筋、四肢\n"
    "  5 - 巽卦 - 胆、股、疏风、安神\n"
    "  6 - 坎卦 - 肾、耳、膀胱、骨、生殖\n"
    "  7 - 艮卦 - 胃、背、鼻、止痛、止\n"
    "  8 - 坤卦 - 脾、腹、肌肉、消化\n\n"
    "使用方法：\n"
    "  1. 默念法：安静状态下，心中默念象数，\n"
    "     如 640·70，每次15-30分钟，每日2-3次。\n"
    "  2. 贴敷法：将象数写在胶布上，贴于相应穴位。\n"
    "  3. 顺序：按配方中的顺序默念，·代表短暂停顿。\n\n"
    "注意事项：\n"
    "  - 本疗法为辅助调理，不能替代正规医疗。\n"
    "  - 急重症请立即就医。\n"
    "  - 孕妇、严重心脏病患者请在专业人士指导下使用。\n"
    "  - 象数疗法需要坚持使用，效果因人而异。\n"
)


class XiangshuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("八卦象数疗法查询系统")
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f5f5f5")
        self.setup_ui()

    def setup_ui(self):
        # ========== 顶部搜索栏 ==========
        frm_top = tk.Frame(self.root, bg="#e8f4fd", height=80)
        frm_top.pack(fill="x", padx=12, pady=(12, 6))
        frm_top.pack_propagate(False)

        tk.Label(
            frm_top, text=" 输入症状关键词：", font=("微软雅黑", 13, "bold"),
            bg="#e8f4fd", fg="#1565c0",
        ).pack(side="left", padx=(18, 8), pady=25)

        self.var_search = tk.StringVar()
        # 绑定输入变化，实时筛选右侧症状列表
        self.var_search.trace_add("write", lambda *_: self.filter_symptom_list())

        entry = tk.Entry(
            frm_top, textvariable=self.var_search,
            font=("微软雅黑", 13), width=30,
            relief="solid", bd=2,
        )
        entry.pack(side="left", pady=22)
        entry.bind("<Return>", lambda e: self.do_search())
        entry.focus_set()

        tk.Button(
            frm_top, text="查 询", font=("微软雅黑", 11, "bold"),
            bg="#42a5f5", fg="white", relief="flat",
            padx=20, pady=6, cursor="hand2",
            command=self.do_search,
        ).pack(side="left", padx=12, pady=22)

        tk.Button(
            frm_top, text="清 空", font=("微软雅黑", 11),
            bg="#ef5350", fg="white", relief="flat",
            padx=14, pady=6, cursor="hand2",
            command=self.do_clear,
        ).pack(side="left", pady=22)

        tk.Button(
            frm_top, text="基础知识", font=("微软雅黑", 10),
            bg="#66bb6a", fg="white", relief="flat",
            padx=12, pady=6, cursor="hand2",
            command=self.show_basic_knowledge,
        ).pack(side="right", padx=(0, 18), pady=22)

        # ========== 快捷按钮栏 ==========
        frm_quick = tk.Frame(self.root, bg="#fff9c4", height=50)
        frm_quick.pack(fill="x", padx=12, pady=(0, 6))
        frm_quick.pack_propagate(False)

        tk.Label(
            frm_quick, text="快捷：", font=("微软雅黑", 10),
            bg="#fff9c4", fg="#f57f17",
        ).pack(side="left", padx=(12, 6), pady=14)

        for sym in COMMON_SYMPTOMS[:14]:
            tk.Button(
                frm_quick, text=sym, font=("微软雅黑", 9),
                bg="#fff176", fg="#e65100", relief="flat",
                padx=8, pady=3, cursor="hand2",
                command=lambda s=sym: self.quick_search(s),
            ).pack(side="left", padx=3, pady=12)

        # ========== 主区域：左侧结果 + 右侧症状清单 ==========
        frm_main = tk.Frame(self.root, bg="white", relief="solid", bd=1)
        frm_main.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        # 用 pack 的 left/right 替代 PanedWindow，更简单稳定
        # 右侧症状清单
        frm_right = tk.Frame(frm_main, bg="#f9fbe7", width=260)
        frm_right.pack(side="right", fill="y", padx=(4, 0))
        frm_right.pack_propagate(False)

        tk.Label(
            frm_right, text="  所有症状（点击搜索）",
            font=("微软雅黑", 10, "bold"),
            bg="#c0ca33", fg="white", anchor="w",
        ).pack(fill="x", padx=0, pady=0)

        # 症状列表 + 滚动条
        frm_list = tk.Frame(frm_right, bg="#f9fbe7")
        frm_list.pack(fill="both", expand=True, padx=4, pady=(2, 4))

        self.lst_symptoms = tk.Listbox(
            frm_list, font=("微软雅黑", 9),
            bg="white", fg="#33691e",
            selectbackground="#aed581",
            selectforeground="#1b5e20",
            relief="solid", bd=1,
            activestyle="none", highlightthickness=0,
        )
        self.lst_symptoms.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(frm_list, command=self.lst_symptoms.yview, width=14)
        sb.pack(side="right", fill="y")
        self.lst_symptoms.config(yscrollcommand=sb.set)

        # 绑定：单击填搜索框，双击直接搜索
        self.lst_symptoms.bind("<ButtonRelease-1>", self.on_symptom_click)
        self.lst_symptoms.bind("<Double-Button-1>", self.on_symptom_doubleclick)

        # 左侧结果区
        frm_left = tk.Frame(frm_main, bg="white")
        frm_left.pack(side="left", fill="both", expand=True)

        self.txt_result = scrolledtext.ScrolledText(
            frm_left, font=("微软雅黑", 11), wrap="word",
            bg="white", fg="#212121",
            padx=16, pady=16,
            insertbackground="#42a5f5", relief="flat",
        )
        self.txt_result.pack(fill="both", expand=True, padx=3, pady=3)

        # ========== 状态栏 ==========
        self.status = tk.StringVar()
        self.status.set("就绪 | 共 %d 条配方，%d 个症状关键词" % (len(RECIPES), len(ALL_SYMPTOMS)))
        tk.Label(
            self.root, textvariable=self.status,
            font=("微软雅黑", 9), bg="#37474f", fg="white",
            anchor="w", padx=15, pady=6,
        ).pack(fill="x", side="bottom")

        self.populate_symptom_list()
        self.show_welcome()

    # ========== 症状列表方法 ==========

    def populate_symptom_list(self, filter_text=""):
        """填充右侧症状列表，支持筛选"""
        self.lst_symptoms.delete(0, "end")
        for sym in ALL_SYMPTOMS:
            if not filter_text or filter_text in sym:
                self.lst_symptoms.insert("end", sym)

    def filter_symptom_list(self):
        """搜索框输入时实时调用"""
        kw = self.var_search.get().strip()
        self.populate_symptom_list(kw)

    def on_symptom_click(self, event):
        """单击：把症状填入搜索框"""
        selection = self.lst_symptoms.curselection()
        if selection:
            sym = self.lst_symptoms.get(selection[0])
            self.var_search.set(sym)

    def on_symptom_doubleclick(self, event):
        """双击：直接搜索该症状"""
        selection = self.lst_symptoms.curselection()
        if selection:
            sym = self.lst_symptoms.get(selection[0])
            self.var_search.set(sym)
            self._search_and_display(sym)

    # ========== 搜索与展示 ==========

    def show_welcome(self):
        self.txt_result.delete("1.0", "end")
        lines = [
            "=" * 58,
            "  八卦象数疗法查询系统",
            "  八卦象数疗法 - 李山玉创立",
            "=" * 58,
            "",
            "使用方法：",
            "  1. 在上方输入框输入症状关键词，点击「查询」",
            "  2. 或点击快捷按钮快速查询常见病",
            "  3. 右侧症状清单：输入时自动筛选，点击搜索",
            "  4. 双击查询结果中的象数可复制到剪贴板",
            "",
            "当前数据库：%d 条配方，%d 个症状关键词" % (len(RECIPES), len(ALL_SYMPTOMS)),
            "",
            "示例关键词：头痛、感冒、咳嗽、失眠、腰痛、",
            "            糖尿病、阳痿、近视、湿疹、痛经",
        ]
        for line in lines:
            self.txt_result.insert("end", line + "\n")

    def do_search(self):
        kw = self.var_search.get().strip()
        if not kw:
            messagebox.showwarning("提示", "请输入症状关键词")
            return
        self._search_and_display(kw)

    def quick_search(self, kw):
        self.var_search.set(kw)
        self._search_and_display(kw)

    def _search_and_display(self, kw):
        results = []
        for r in RECIPES:
            for s in r["symptoms"]:
                if kw in s:
                    results.append(r)
                    break

        self.txt_result.delete("1.0", "end")

        if not results:
            self.txt_result.insert("end", "=" * 58 + "\n")
            self.txt_result.insert("end", "  未找到「%s」相关配方\n" % kw)
            self.txt_result.insert("end", "=" * 58 + "\n\n")
            self.txt_result.insert("end", "建议：\n")
            self.txt_result.insert("end", "  - 尝试更简短的关键词（如「痛」、「炎」）\n")
            self.txt_result.insert("end", "  - 检查是否有错别字\n")
            self.txt_result.insert("end", "  - 从右侧症状清单中选择\n")
            self.status.set("未找到「%s」相关配方" % kw)
            return

        self.txt_result.insert("end", "=" * 58 + "\n")
        self.txt_result.insert("end", "  「%s」找到 %d 条配方\n" % (kw, len(results)))
        self.txt_result.insert("end", "=" * 58 + "\n\n")

        for i, r in enumerate(results, 1):
            syms = "、".join(r["symptoms"])
            formula = r["formula"]
            self.txt_result.insert("end", "【%d】症状：%s\n" % (i, syms), "symptom")
            self.txt_result.insert("end", "    象数：", "label")
            self.txt_result.insert("end", "%s\n" % formula, ("formula", "clickable"))
            self.txt_result.insert("end", "    方义：%s\n\n" % r["explanation"])

        self.txt_result.tag_config("symptom", font=("微软雅黑", 11, "bold"), foreground="#1565c0")
        self.txt_result.tag_config("label", font=("微软雅黑", 10), foreground="#555")
        self.txt_result.tag_config("formula", font=("Courier New", 13, "bold"), foreground="#d32f2f", background="#fff9c4")
        self.txt_result.tag_config("clickable", font=("Courier New", 13, "bold"), foreground="#d32f2f", background="#fff9c4")
        self.txt_result.tag_bind("clickable", "<Double-Button-1>", lambda e: self.copy_formula(e))

        self.status.set("「%s」找到 %d 条配方 | 双击象数可复制" % (kw, len(results)))

    def copy_formula(self, event):
        try:
            index = self.txt_result.index("@%d,%d" % (event.x, event.y))
            line = self.txt_result.get(index + " linestart", index + " lineend")
            m = re.search(r"[\d·]+", line)
            if m:
                formula = m.group()
                self.root.clipboard_clear()
                self.root.clipboard_append(formula)
                self.status.set("已复制象数：%s" % formula)
        except Exception:
            pass

    def do_clear(self):
        self.var_search.set("")
        self.populate_symptom_list()
        self.show_welcome()

    def show_basic_knowledge(self):
        win = tk.Toplevel(self.root)
        win.title("八卦象数疗法基础知识")
        win.geometry("620x550")
        win.configure(bg="white")

        txt = scrolledtext.ScrolledText(
            win, font=("微软雅黑", 11), wrap="word",
            bg="white", fg="#212121",
            padx=15, pady=15, relief="flat",
        )
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("end", BASIC_KNOWLEDGE)
        txt.config(state="disabled")


def main():
    root = tk.Tk()
    app = XiangshuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
