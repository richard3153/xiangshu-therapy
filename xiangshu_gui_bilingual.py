#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八卦象数疗法 - 双语 GUI (tkinter)
True bilingual: Chinese / English switch via top-right button.
Data source: xiangshu_data.py (CN) or xiangshu_data_en.py (EN)
v2.1: language toggle, dynamic label update, bug-fixed
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import importlib.util, sys, os, re

# --- Load data modules ---
def load_data_module(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    spec = importlib.util.spec_from_file_location("data_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.RECIPES

try:
    RECIPES_CN = load_data_module("xiangshu_data.py")
    ALL_SYMPTOMS_CN = sorted(set(s for r in RECIPES_CN for s in r["symptoms"]))
except Exception as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"Cannot load xiangshu_data.py:\n{e}")
    raise SystemExit(1)

try:
    RECIPES_EN = load_data_module("xiangshu_data_en.py")
    ALL_SYMPTOMS_EN = sorted(set(s for r in RECIPES_EN for s in r["symptoms"]))
except Exception:
    RECIPES_EN = RECIPES_CN
    ALL_SYMPTOMS_EN = ALL_SYMPTOMS_CN

# --- UI Text dictionaries ---
UI = {
    "CN": {
        "title": "八卦象数疗法查询系统",
        "search_label": " 输入症状关键词：",
        "btn_search": "查 询",
        "btn_clear": "清 空",
        "btn_basic": "基础知识",
        "quick_label": "快捷：",
        "symptom_list_title": "  所有症状（点击搜索）",
        "status_ready": "就绪 | 共 %d 条配方，%d 个症状关键词",
        "welcome": [
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
            "当前数据库：%d 条配方，%d 个症状关键词",
            "",
            "示例关键词：头痛、感冒、咳嗽、失眠、腰痛、",
            "            糖尿病、阳痿、近视、湿疹、痛经",
        ],
        "not_found": "未找到「%s」相关配方",
        "not_found_suggest": "建议：\n  - 尝试更简短的关键词（如「痛」、「炎」）\n  - 检查是否有错别字\n  - 从右侧症状清单中选择",
        "result_header": "  找到 %d 条「%s」相关配方",
        "copy_formula": "已复制象数：%s",
        "basic_title": "八卦象数疗法基础知识",
        "basic_content": (
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
        ),
        "warn_input": "请输入症状关键词",
        "common_symptoms": [
            "头痛", "偏头痛", "感冒", "咳嗽", "失眠", "多梦",
            "腰痛", "胃痛", "关节炎", "高血压", "糖尿病",
            "近视", "耳鸣", "鼻炎", "口腔溃疡", "牙痛",
            "湿疹", "痤疮", "痛经", "更年期", "抑郁",
            "面瘫", "帕金森", "偏瘫", "坐骨神经痛",
            "颈椎病", "肩周炎", "静脉曲张", "脱发",
            "阳痿", "遗精", "前列腺炎", "肾结石",
            "肥胖", "戒烟", "解酒", "晕车", "美白",
        ],
        "lang_btn": "EN",
    },
    "EN": {
        "title": "Eight Diagrams Numerology Therapy",
        "search_label": " Enter symptom keyword:",
        "btn_search": "Search",
        "btn_clear": "Clear",
        "btn_basic": "Basics",
        "quick_label": "Quick:",
        "symptom_list_title": "  All Symptoms (click to search)",
        "status_ready": "Ready | %d recipes, %d symptoms",
        "welcome": [
            "=" * 62,
            "  Eight Diagrams Numerology Therapy",
            "  (Bagua Xiang Shu Therapy - by Li Shanyu)",
            "=" * 62,
            "",
            "How to use:",
            "  1. Type a symptom keyword above, click [Search]",
            "  2. Or click a Quick button for common symptoms",
            "  3. Right panel: symptoms filter as you type, click to search",
            "  4. Double-click a formula in results to copy to clipboard",
            "",
            "Database: %d recipes, %d symptom keywords",
            "",
            "Example keywords: headache, migraine, cold, cough, insomnia,",
            "       diabetes, impotence, myopia, eczema, dysmenorrhea",
        ],
        "not_found": "No recipes found for '%s'",
        "not_found_suggest": "Suggestions:\n  - Try a shorter keyword (e.g. 'pain', 'itis')\n  - Check spelling\n  - Select from the symptom list on the right",
        "result_header": "  Found %d recipe(s) for '%s'",
        "copy_formula": "Copied formula: %s",
        "basic_title": "Basic Knowledge of XiangShu Therapy",
        "basic_content": (
            "Basic Knowledge of Eight Diagrams Numerology Therapy\n"
            "=" * 55 + "\n\n"
            "XiangShu Therapy is a natural therapy created by Li Shanyu,\n"
            "which regulates the body by silently reciting or applying\n"
            "specific number combinations (XiangShu).\n\n"
            "Bagua - Number Correspondence:\n"
            "  1 - Qian - Head, brain, Du meridian, Large intestine\n"
            "  2 - Dui  - Lung, nose, throat, skin\n"
            "  3 - Li   - Heart, eyes, blood, tongue\n"
            "  4 - Zhen - Liver, gallbladder, tendons, limbs\n"
            "  5 - Xun  - Gallbladder, thigh, dispel wind, calm spirit\n"
            "  6 - Kan  - Kidney, ears, bladder, bone, reproduction\n"
            "  7 - Gen  - Stomach, back, nose, stop pain\n"
            "  8 - Kun  - Spleen, abdomen, muscle, digestion\n\n"
            "How to use:\n"
            "  1. Silent recitation: in a quiet state, mentally recite\n"
            "     the numbers, e.g. 640·70, 15-30 min, 2-3 times/day.\n"
            "  2. Patch method: write numbers on adhesive tape,\n"
            "     apply to corresponding acupoints.\n"
            "  3. Order: recite in the order shown; · means a short pause.\n\n"
            "Cautions:\n"
            "  - This therapy is complementary, NOT a substitute for medical care.\n"
            "  - Seek immediate medical attention for acute/severe conditions.\n"
            "  - Pregnant women and patients with serious heart disease:\n"
            "    use only under professional guidance.\n"
            "  - Consistent use is required; effects vary by individual.\n"
        ),
        "warn_input": "Please enter a symptom keyword",
        "common_symptoms": [
            "headache", "migraine", "cold", "cough", "insomnia", "dreams",
            "low back pain", "stomach pain", "arthritis", "hypertension", "diabetes",
            "myopia", "tinnitus", "rhinitis", "oral ulcer", "toothache",
            "eczema", "acne", "dysmenorrhea", "menopause", "depression",
            "facial paralysis", "Parkinson's", "hemiplegia", "sciatica",
            "cervical spondylosis", "frozen shoulder", "varicose veins", "hair loss",
            "impotence", "spontaneous emission", "prostatitis", "kidney stones",
            "obesity", "smoking cessation", "sober up", "carsickness", "skin whitening",
        ],
        "lang_btn": "中",
    },
}


class XiangshuApp:
    def __init__(self, root):
        self.root = root
        self.lang = "CN"
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f5f5f5")
        self.setup_ui()
        self.apply_lang()

    # ----------------------------------------------------------------
    #  UI setup (widgets created once, text updated via apply_lang)
    # ----------------------------------------------------------------
    def setup_ui(self):
        # ---- Top search bar ----
        self.frm_top = tk.Frame(self.root, height=80)
        self.frm_top.pack(fill="x", padx=12, pady=(12, 6))
        self.frm_top.pack_propagate(False)

        self.lbl_search = tk.Label(self.frm_top)
        self.lbl_search.pack(side="left", padx=(18, 8), pady=25)

        self.var_search = tk.StringVar()
        self.var_search.trace_add("write", lambda *_: self.filter_symptom_list())

        self.entry_search = tk.Entry(
            self.frm_top, textvariable=self.var_search,
            font=("Microsoft YaHei", 13), width=30,
            relief="solid", bd=2,
        )
        self.entry_search.pack(side="left", pady=22)
        self.entry_search.bind("<Return>", lambda e: self.do_search())
        self.entry_search.focus_set()

        self.btn_search = tk.Button(self.frm_top, relief="flat", cursor="hand2",
                                   command=self.do_search)
        self.btn_search.pack(side="left", padx=12, pady=22)

        self.btn_clear = tk.Button(self.frm_top, relief="flat", cursor="hand2",
                                  command=self.do_clear)
        self.btn_clear.pack(side="left", pady=22)

        # Language toggle button (top right)
        self.btn_lang = tk.Button(self.frm_top, font=("Arial", 11, "bold"),
                                  relief="raised", bd=2, cursor="hand2",
                                  command=self.toggle_lang)
        self.btn_lang.pack(side="right", padx=(0, 18), pady=22)

        self.btn_basic = tk.Button(self.frm_top, relief="flat", cursor="hand2",
                                  command=self.show_basic_knowledge)
        self.btn_basic.pack(side="right", padx=(0, 8), pady=22)

        # ---- Quick buttons bar ----
        self.frm_quick = tk.Frame(self.root)
        self.frm_quick.pack(fill="x", padx=12, pady=(0, 6))
        self.frm_quick.pack_propagate(False)

        self.lbl_quick = tk.Label(self.frm_quick)
        self.lbl_quick.pack(side="left", padx=(12, 6), pady=14)

        self.quick_buttons = []
        for i in range(14):
            btn = tk.Button(self.frm_quick, relief="flat", cursor="hand2")
            btn.pack(side="left", padx=3, pady=12)
            self.quick_buttons.append(btn)

        # ---- Main area: left results + right symptom list ----
        frm_main = tk.Frame(self.root, relief="solid", bd=1)
        frm_main.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        # Right panel: symptom list
        frm_right = tk.Frame(frm_main, width=260)
        frm_right.pack(side="right", fill="y", padx=(4, 0))
        frm_right.pack_propagate(False)

        self.lbl_symptom_list = tk.Label(frm_right, anchor="w")
        self.lbl_symptom_list.pack(fill="x", padx=0, pady=0)

        frm_list = tk.Frame(frm_right)
        frm_list.pack(fill="both", expand=True, padx=4, pady=(2, 4))

        self.lst_symptoms = tk.Listbox(
            frm_list, activestyle="none", highlightthickness=0,
        )
        self.lst_symptoms.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(frm_list, command=self.lst_symptoms.yview, width=14)
        sb.pack(side="right", fill="y")
        self.lst_symptoms.config(yscrollcommand=sb.set)

        self.lst_symptoms.bind("<ButtonRelease-1>", self.on_symptom_click)
        self.lst_symptoms.bind("<Double-Button-1>", self.on_symptom_doubleclick)

        # Left panel: results
        frm_left = tk.Frame(frm_main)
        frm_left.pack(side="left", fill="both", expand=True)

        self.txt_result = scrolledtext.ScrolledText(
            frm_left, font=("Microsoft YaHei", 11), wrap="word",
            relief="flat", padx=16, pady=16,
        )
        self.txt_result.pack(fill="both", expand=True, padx=3, pady=3)

        # ---- Status bar ----
        self.status = tk.StringVar()
        self.lbl_status = tk.Label(
            self.root, textvariable=self.status,
            font=("Microsoft YaHei", 9), anchor="w",
            padx=15, pady=6,
        )
        self.lbl_status.pack(fill="x", side="bottom")

        self.populate_symptom_list()
        self.show_welcome()

    # ----------------------------------------------------------------
    #  Language switch
    # ----------------------------------------------------------------
    def toggle_lang(self):
        self.lang = "EN" if self.lang == "CN" else "CN"
        self.apply_lang()

    def apply_lang(self):
        T = UI[self.lang]
        is_cn = self.lang == "CN"

        self.root.title(T["title"])

        # Top bar colors & fonts
        if is_cn:
            bg_top, fg_top, font_top = "#e8f4fd", "#1565c0", ("Microsoft YaHei", 13, "bold")
            bg_q, fg_q, font_q = "#fff9c4", "#f57f17", ("Microsoft YaHei", 10)
            bg_btn, fg_btn = "#42a5f5", "white"
            bg_clr, fg_clr = "#ef5350", "white"
            bg_bsc, fg_bsc = "#66bb6a", "white"
            bg_lbl, fg_lbl = "#c0ca33", "white"
            font_lbl = ("Microsoft YaHei", 10, "bold")
        else:
            bg_top, fg_top, font_top = "#e3f2fd", "#1565c0", ("Arial", 12, "bold")
            bg_q, fg_q, font_q = "#e8eaf6", "#303f9f", ("Arial", 10)
            bg_btn, fg_btn = "#42a5f5", "white"
            bg_clr, fg_clr = "#ef5350", "white"
            bg_bsc, fg_bsc = "#66bb6a", "white"
            bg_lbl, fg_lbl = "#5c6bc0", "white"
            font_lbl = ("Arial", 10, "bold")

        self.frm_top.configure(bg=bg_top)
        self.lbl_search.configure(bg=bg_top, fg=fg_top, font=font_top)

        self.btn_search.configure(
            text=T["btn_search"], bg=bg_btn, fg=fg_btn,
            font=("Microsoft YaHei", 11, "bold") if is_cn else ("Arial", 11, "bold"),
            padx=20, pady=6,
        )
        self.btn_clear.configure(
            text=T["btn_clear"], bg=bg_clr, fg=fg_clr,
            font=("Microsoft YaHei", 11) if is_cn else ("Arial", 11),
            padx=14, pady=6,
        )
        self.btn_basic.configure(
            text=T["btn_basic"], bg=bg_bsc, fg=fg_bsc,
            font=("Microsoft YaHei", 10) if is_cn else ("Arial", 10),
            padx=12, pady=6,
        )
        self.btn_lang.configure(text=T["lang_btn"],
                              bg="#ffcc02" if is_cn else "#e0e0e0",
                              fg="#212121",
                              padx=12, pady=5)

        # Quick bar
        self.frm_quick.configure(bg=bg_q)
        self.lbl_quick.configure(bg=bg_q, fg=fg_q, font=font_q)

        for i, btn in enumerate(self.quick_buttons):
            sym = T["common_symptoms"][i] if i < len(T["common_symptoms"]) else ""
            btn.configure(
                text=sym,
                font=("Microsoft YaHei", 9) if is_cn else ("Arial", 9),
                bg="#fff176" if is_cn else "#c5cae9",
                fg="#e65100" if is_cn else "#1a237e",
                command=lambda s=sym: self.quick_search(s) if s else None,
            )

        # Right panel
        self.lbl_symptom_list.configure(
            text=T["symptom_list_title"],
            bg=bg_lbl, fg=fg_lbl, font=font_lbl,
        )
        self.lst_symptoms.configure(
            font=("Microsoft YaHei", 9) if is_cn else ("Arial", 9),
            bg="white",
            fg="#33691e" if is_cn else "#1b5e20",
            selectbackground="#aed581",
            selectforeground="#1b5e20",
        )

        # Status bar
        rec = RECIPES_CN if is_cn else RECIPES_EN
        sym = ALL_SYMPTOMS_CN if is_cn else ALL_SYMPTOMS_EN
        self.lbl_status.configure(
            bg="#37474f" if is_cn else "#263238", fg="white",
            font=("Microsoft YaHei", 9) if is_cn else ("Arial", 9),
        )
        self.status.set(T["status_ready"] % (len(rec), len(sym)))

        # Refresh symptom list for current language
        self.populate_symptom_list()
        self.show_welcome()

    # ----------------------------------------------------------------
    #  Symptom list
    # ----------------------------------------------------------------
    def populate_symptom_list(self, filter_text=""):
        self.lst_symptoms.delete(0, "end")
        syms = ALL_SYMPTOMS_CN if self.lang == "CN" else ALL_SYMPTOMS_EN
        for s in syms:
            if not filter_text or filter_text.lower() in s.lower():
                self.lst_symptoms.insert("end", s)

    def filter_symptom_list(self):
        kw = self.var_search.get().strip()
        self.populate_symptom_list(kw)

    def on_symptom_click(self, event):
        selection = self.lst_symptoms.curselection()
        if selection:
            self.var_search.set(self.lst_symptoms.get(selection[0]))

    def on_symptom_doubleclick(self, event):
        selection = self.lst_symptoms.curselection()
        if selection:
            sym = self.lst_symptoms.get(selection[0])
            self.var_search.set(sym)
            self._search_and_display(sym)

    # ----------------------------------------------------------------
    #  Search
    # ----------------------------------------------------------------
    def show_welcome(self):
        self.txt_result.delete("1.0", "end")
        T = UI[self.lang]
        rec = RECIPES_CN if self.lang == "CN" else RECIPES_EN
        syms = ALL_SYMPTOMS_CN if self.lang == "CN" else ALL_SYMPTOMS_EN
        for line in T["welcome"]:
            if "%d" in line:
                line = line % (len(rec), len(syms))
            self.txt_result.insert("end", line + "\n")

    def do_search(self):
        kw = self.var_search.get().strip()
        if not kw:
            messagebox.showwarning("提示" if self.lang == "CN" else "Hint",
                                  UI[self.lang]["warn_input"])
            return
        self._search_and_display(kw)

    def quick_search(self, kw):
        if not kw:
            return
        self.var_search.set(kw)
        self._search_and_display(kw)

    def _search_and_display(self, kw):
        rec = RECIPES_CN if self.lang == "CN" else RECIPES_EN
        results = []
        for r in rec:
            for s in r["symptoms"]:
                if kw.lower() in s.lower():
                    results.append(r)
                    break

        self.txt_result.delete("1.0", "end")
        T = UI[self.lang]

        if not results:
            self.txt_result.insert("end", "=" * 58 + "\n")
            self.txt_result.insert("end", "  " + T["not_found"] % kw + "\n")
            self.txt_result.insert("end", "=" * 58 + "\n\n")
            self.txt_result.insert("end", T["not_found_suggest"] + "\n")
            self.status.set(T["not_found"] % kw)
            return

        self.txt_result.insert("end", "=" * 58 + "\n")
        self.txt_result.insert("end", "  " + T["result_header"] % (len(results), kw) + "\n")
        self.txt_result.insert("end", "=" * 58 + "\n\n")

        for i, r in enumerate(results, 1):
            syms = ", ".join(r["symptoms"])
            formula = r["formula"]
            self.txt_result.insert("end", "[%d] Symptoms: %s\n" % (i, syms), "symptom")
            self.txt_result.insert("end", "    Formula: ", "label")
            self.txt_result.insert("end", "%s\n" % formula, ("formula", "clickable"))
            self.txt_result.insert("end", "    Note: %s\n\n" % r["explanation"])

        self._config_result_tags()
        self.status.set(T["result_header"] % (len(results), kw))

    def _config_result_tags(self):
        is_cn = self.lang == "CN"
        self.txt_result.tag_config("symptom",
            font=("Microsoft YaHei", 11, "bold") if is_cn else ("Arial", 11, "bold"),
            foreground="#1565c0" if is_cn else "#1565c0")
        self.txt_result.tag_config("label",
            font=("Microsoft YaHei", 10) if is_cn else ("Arial", 10),
            foreground="#555")
        self.txt_result.tag_config("formula",
            font=("Courier New", 13, "bold"),
            foreground="#d32f2f",
            background="#fff9c4")
        self.txt_result.tag_bind("clickable", "<Double-Button-1>", lambda e: self.copy_formula(e))

    def copy_formula(self, event):
        try:
            index = self.txt_result.index("@%d,%d" % (event.x, event.y))
            line = self.txt_result.get(index + " linestart", index + " lineend")
            m = re.search(r"[\d·]+", line)
            if m:
                formula = m.group()
                self.root.clipboard_clear()
                self.root.clipboard_append(formula)
                self.status.set(UI[self.lang]["copy_formula"] % formula)
        except Exception:
            pass

    def do_clear(self):
        self.var_search.set("")
        self.populate_symptom_list()
        self.show_welcome()

    def show_basic_knowledge(self):
        T = UI[self.lang]
        win = tk.Toplevel(self.root)
        win.title(T["basic_title"])
        win.geometry("660x580")
        win.configure(bg="white")

        txt = scrolledtext.ScrolledText(
            win, font=("Microsoft YaHei", 11) if self.lang == "CN" else ("Arial", 11),
            wrap="word", bg="white", fg="#212121",
            padx=15, pady=15, relief="flat",
        )
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("end", T["basic_content"])
        txt.config(state="disabled")


def main():
    root = tk.Tk()
    app = XiangshuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
