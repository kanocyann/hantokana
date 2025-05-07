import sys
import jaconv
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
import tkinter as tk
from tkinter import Menu, filedialog
import os
import json
from ctypes import windll
from PIL import Image, ImageTk

# 高清支持
windll.shcore.SetProcessDpiAwareness(1)

# 全局变量
custom_dict = {
    "normal_words": {},
    "compound_words": {}
}
current_dict_path = None  # 跟踪当前使用的字典路径
tagger = None  # 初始化 tagger
conv = None  # 初始化 conv


def resource_path(relative_path):
    """获取资源的绝对路径，适用于开发环境和PyInstaller打包环境"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_appdata_path():
    """获取应用程序数据目录路径"""
    appdata = os.getenv('APPDATA')
    app_dir = os.path.join(appdata, 'Hantokana')
    os.makedirs(app_dir, exist_ok=True)
    return app_dir


def get_dict_path():
    """获取字典文件永久存储路径"""
    return os.path.join(get_appdata_path(), 'custom_dict.json')


def get_config_path():
    """获取配置文件路径"""
    return os.path.join(get_appdata_path(), 'config.json')


# 延迟导入模块
def init_tagger():
    try:
        from fugashi import Tagger
        tagger = Tagger('-r "' + resource_path('dicdir/mecabrc') + '" -d "' + resource_path('dicdir') + '"')
    except Exception:
        from fugashi import Tagger
        tagger = Tagger()
    return tagger


def init_kks():
    import pykakasi
    kks = pykakasi.kakasi()
    # 使用新的API设置模式
    kks.setMode("J", "a")
    kks.setMode("K", "a")
    kks.setMode("H", "a")
    kks.setMode("r", "Hepburn")
    return kks.getConverter()


def load_config():
    """加载配置文件"""
    global current_dict_path
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                current_dict_path = config.get('dict_path')
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")


def load_custom_dict():
    """加载自定义词典"""
    global custom_dict, current_dict_path
    if current_dict_path and os.path.exists(current_dict_path):
        custom_dict_path = current_dict_path
    else:
        custom_dict_path = get_dict_path()

    if not os.path.exists(custom_dict_path):
        try:
            initial_dict_path = resource_path("custom_dict.json")
            if os.path.exists(initial_dict_path):
                with open(initial_dict_path, "r", encoding="utf-8") as src:
                    data = src.read()
                with open(custom_dict_path, "w", encoding="utf-8") as dst:
                    dst.write(data)
            else:
                with open(custom_dict_path, "w", encoding="utf-8") as f:
                    json.dump({
                        "normal_words": {},
                        "compound_words": {}
                    }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"初始化字典文件失败: {str(e)}")

    try:
        with open(custom_dict_path, "r", encoding="utf-8") as f:
            custom_dict = json.load(f)
        current_dict_path = custom_dict_path
    except Exception as e:
        print(f"加载字典文件失败: {str(e)}")
        custom_dict = {
            "normal_words": {},
            "compound_words": {}
        }


def save_custom_dict():
    """保存自定义词典"""
    global custom_dict, current_dict_path
    dict_path = current_dict_path or get_dict_path()
    os.makedirs(os.path.dirname(dict_path), exist_ok=True)
    try:
        with open(dict_path, "w", encoding="utf-8") as f:
            json.dump(custom_dict, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存字典文件失败: {str(e)}")


def set_window_icon(window):
    """设置窗口图标"""
    try:
        window.iconbitmap(resource_path("icon.ico"))
    except Exception:
        pass


def show_message(parent, title, message, style='info'):
    """显示带图标的消息框"""
    dialog = tb.Toplevel(parent)
    dialog.title(title)
    set_window_icon(dialog)

    frame = tb.Frame(dialog, padding=10)
    frame.pack(fill=BOTH, expand=True)

    icon_mapping = {
        'info': ('✓', 'success'),
        'warning': ('⚠', 'warning'),
        'error': ('✗', 'danger')
    }
    icon, color = icon_mapping.get(style, ('i', 'info'))

    tb.Label(frame, text=icon, font=("Segoe UI", 24), bootstyle=color).pack(pady=10)
    tb.Label(frame, text=message, font=("Segoe UI", 12)).pack(pady=5)

    tb.Button(frame, text="确定", bootstyle=color, command=dialog.destroy).pack(pady=10)
    dialog.transient(parent)
    dialog.grab_set()

    # 计算消息框位置
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    dialog_width = 340
    dialog_height = 200
    x = parent_x + (parent_width - dialog_width) // 2
    y = parent_y + (parent_height - dialog_height) // 2
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")


def load_dict():
    """加载自定义词典文件"""
    file_path = filedialog.askopenfilename(title="选择自定义词典文件", filetypes=[("JSON 文件", "*.json")])
    if not file_path:
        return
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            new_dict = json.load(f)
        if isinstance(new_dict, dict):
            global custom_dict, current_dict_path
            # 合并字典
            custom_dict["normal_words"] = {**custom_dict["normal_words"], **new_dict.get("normal_words", {})}
            custom_dict["compound_words"] = {**custom_dict["compound_words"], **new_dict.get("compound_words", {})}
            # 确保目标目录存在
            os.makedirs(os.path.dirname(get_dict_path()), exist_ok=True)
            with open(get_dict_path(), "w", encoding="utf-8") as f:
                json.dump(custom_dict, f, ensure_ascii=False, indent=2)
            show_message(root, "成功", "词典导入并合并成功")
        else:
            show_message(root, "警告", "所选文件格式无效，请选择一个有效的 JSON 文件", "warning")
    except Exception as e:
        show_message(root, "错误", f"导入词典时发生错误: {e}", "error")


def split_readings(raw):
    """分割假名字符串为列表"""
    for sep in [",", "，", "、"]:
        raw = raw.replace(sep, ",")
    return [r.strip() for r in raw.split(",") if r.strip()]


def update_dict_view(listbox, word_type):
    """更新词典列表显示"""
    listbox.delete(0, tk.END)
    word_dict = custom_dict[word_type]
    for kanji, readings in sorted(word_dict.items()):
        listbox.insert(tk.END, f"{kanji} → {', '.join(readings)}")


def add_entry(kanji_entry, readings_entry, listbox, edit_window, word_type):
    """添加新词条"""
    kanji = kanji_entry.get().strip()
    readings = split_readings(readings_entry.get().strip())
    if kanji and readings:
        try:
            custom_dict[word_type][kanji] = readings
            save_custom_dict()
            update_dict_view(listbox, word_type)
            kanji_entry.delete(0, tk.END)
            readings_entry.delete(0, tk.END)
            show_message(edit_window, "成功", "词条已添加")
        except Exception as e:
            show_message(edit_window, "错误", f"保存词条时出错: {str(e)}", "error")
            print(f"保存词条时出错: {str(e)}")
    else:
        show_message(edit_window, "警告", "请输入有效的汉字和假名", "warning")


def delete_selected(listbox, edit_window, word_type):
    """删除选中的词条"""
    selected_items = listbox.curselection()
    if not selected_items:
        show_message(edit_window, "警告", "请选择要删除的条目", "warning")
        return

    confirm_dialog = tb.Toplevel(edit_window)
    confirm_dialog.title("确认删除")
    set_window_icon(confirm_dialog)

    # 调整确认退出窗口大小
    dialog_width = 300
    dialog_height = 200

    frame = tb.Frame(confirm_dialog, padding=10)
    frame.pack(fill=BOTH, expand=True)

    tb.Label(frame, text="⚠", font=("Segoe UI", 24), bootstyle="warning").pack(pady=10)
    tb.Label(frame, text=f"确定要删除这 {len(selected_items)} 个条目吗？", font=("Segoe UI", 12)).pack(pady=5)

    button_frame = tb.Frame(frame)
    button_frame.pack(pady=10)

    def do_delete():
        try:
            word_dict = custom_dict[word_type]
            for item in reversed(selected_items):
                selected_kanji = listbox.get(item).split(" → ")[0]
                del word_dict[selected_kanji]

            save_custom_dict()
            update_dict_view(listbox, word_type)
            confirm_dialog.destroy()
            show_message(edit_window, "成功", f"已删除 {len(selected_items)} 个条目")
        except Exception as e:
            show_message(edit_window, "错误", f"删除词条时出错: {str(e)}", "error")

    tb.Button(button_frame, text="确定", bootstyle="danger", command=do_delete).pack(side=LEFT, padx=10)
    tb.Button(button_frame, text="取消", bootstyle="secondary", command=confirm_dialog.destroy).pack(side=RIGHT,
                                                                                                     padx=10)

    # 计算确认对话框位置
    parent_x = edit_window.winfo_x()
    parent_y = edit_window.winfo_y()
    parent_width = edit_window.winfo_width()
    parent_height = edit_window.winfo_height()
    x = parent_x + (parent_width - dialog_width) // 2
    y = parent_y + (parent_height - dialog_height) // 2
    confirm_dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")


def edit_entry(listbox, edit_window, word_type):
    """编辑选中的词条"""
    selected_item = listbox.curselection()
    if selected_item:
        word_dict = custom_dict[word_type]
        selected_kanji = listbox.get(selected_item[0]).split(" → ")[0]
        readings = word_dict[selected_kanji]

        edit_dialog = tb.Toplevel(edit_window)
        edit_dialog.title("编辑词条")
        set_window_icon(edit_dialog)

        main_frame = tb.Frame(edit_dialog, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        input_frame = tb.LabelFrame(main_frame, text="编辑词条内容", padding=10)
        input_frame.pack(fill=BOTH, expand=True, pady=5)

        tb.Label(input_frame, text="汉字", bootstyle="inverse-light").pack(anchor="w")
        kanji_edit = tb.Entry(input_frame, font=("Segoe UI", 12))
        kanji_edit.insert(0, selected_kanji)
        kanji_edit.pack(fill=X, pady=5)

        tb.Label(input_frame, text="对应假名 (用逗号间隔)", bootstyle="inverse-light").pack(anchor="w")
        readings_edit = tb.Entry(input_frame, font=("Segoe UI", 12))
        readings_edit.insert(0, ", ".join(readings))
        readings_edit.pack(fill=X, pady=5)

        button_frame = tb.Frame(main_frame)
        button_frame.pack(fill=X, pady=10)

        def save_edit():
            """保存编辑结果"""
            new_kanji = kanji_edit.get().strip()
            new_readings = split_readings(readings_edit.get().strip())

            if new_kanji and new_readings:
                try:
                    if new_kanji != selected_kanji:
                        del word_dict[selected_kanji]
                    word_dict[new_kanji] = new_readings

                    save_custom_dict()
                    update_dict_view(listbox, word_type)
                    edit_dialog.destroy()
                    show_message(edit_window, "成功", "词条已更新")
                except Exception as e:
                    show_message(edit_dialog, "错误", f"保存修改时出错: {str(e)}", "error")
            else:
                show_message(edit_dialog, "警告", "请输入有效的汉字和假名", "warning")

        tb.Button(button_frame, text="保存", bootstyle="success", command=save_edit).pack(side=LEFT, padx=5)
        tb.Button(button_frame, text="取消", bootstyle="secondary", command=edit_dialog.destroy).pack(side=RIGHT,
                                                                                                      padx=5)

        # 计算编辑对话框位置
        parent_x = edit_window.winfo_x()
        parent_y = edit_window.winfo_y()
        parent_width = edit_window.winfo_width()
        parent_height = edit_window.winfo_height()
        dialog_width = 600
        dialog_height = 300
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        edit_dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    else:
        show_message(edit_window, "警告", "请选择要编辑的条目", "warning")


def copy_selected(listbox, edit_window):
    """复制选中的词条"""
    selected_item = listbox.curselection()
    if selected_item:
        item = listbox.get(selected_item[0])
        edit_window.clipboard_clear()
        edit_window.clipboard_append(item)
        show_message(edit_window, "成功", "已复制选中词条")


def copy_all(listbox, edit_window):
    """复制所有词条"""
    all_text = "\n".join([listbox.get(i) for i in range(listbox.size())])
    edit_window.clipboard_clear()
    edit_window.clipboard_append(all_text)
    show_message(edit_window, "成功", "已复制所有词条")


def setup_context_menu(listbox, edit_window):
    """设置右键上下文菜单"""
    context_menu = Menu(edit_window, tearoff=0)
    context_menu.add_command(label="复制", command=lambda: copy_selected(listbox, edit_window))
    context_menu.add_command(label="编辑", command=lambda: edit_entry(listbox, edit_window))
    context_menu.add_command(label="删除", command=lambda: delete_selected(listbox, edit_window))

    def show_context_menu(event):
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    listbox.bind("<Button-3>", show_context_menu)


def open_edit_dict_window(word_type):
    """打开词典编辑窗口"""
    edit_window = tb.Toplevel(root)
    edit_window.title(f"编辑{'复合词' if word_type == 'compound_words' else '普通词'}词典")
    set_window_icon(edit_window)

    dict_frame = tb.Frame(edit_window, padding=10)
    dict_frame.pack(fill=BOTH, expand=True)

    # 显示当前词典文件路径的标签
    path_label = tb.Label(dict_frame, text=f"当前词典文件路径: {current_dict_path}", bootstyle="inverse-light")
    path_label.pack(anchor="w", pady=5)

    # 输入区域
    input_frame = tb.LabelFrame(dict_frame, text=f"添加新{'复合词' if word_type == 'compound_words' else '普通词'}词条",
                                padding=10)
    input_frame.pack(fill=X, pady=5)

    tb.Label(input_frame, text=f"{'复合词' if word_type == 'compound_words' else '汉字'}",
             bootstyle="inverse-light").pack(anchor="w")
    kanji_entry = tb.Entry(input_frame, font=("Segoe UI", 12))
    kanji_entry.pack(fill=X, pady=5)

    tb.Label(input_frame, text="对应假名 (用逗号间隔)", bootstyle="inverse-light").pack(anchor="w")
    readings_entry = tb.Entry(input_frame, font=("Segoe UI", 12))
    readings_entry.pack(fill=X, pady=5)

    # 按钮区域
    button_frame = tb.Frame(dict_frame)
    button_frame.pack(fill=X, pady=5)

    tb.Button(button_frame, text="添加词条", bootstyle="success",
              command=lambda: add_entry(kanji_entry, readings_entry, listbox, edit_window, word_type)).pack(side=LEFT,
                                                                                                            padx=5)
    tb.Button(button_frame, text="编辑词条", bootstyle="info",
              command=lambda: edit_entry(listbox, edit_window, word_type)).pack(side=LEFT, padx=5)
    tb.Button(button_frame, text="删除选中", bootstyle="danger",
              command=lambda: delete_selected(listbox, edit_window, word_type)).pack(side=LEFT, padx=5)
    tb.Button(button_frame, text="复制全部", bootstyle="secondary",
              command=lambda: copy_all(listbox, edit_window)).pack(side=RIGHT, padx=5)

    # 词典列表区域
    list_frame = tb.LabelFrame(dict_frame, text="词典内容", padding=10)
    list_frame.pack(fill=BOTH, expand=True, pady=5)

    listbox = tk.Listbox(list_frame, font=("Segoe UI", 12), selectmode=tk.EXTENDED)
    listbox.pack(fill=BOTH, expand=True)

    scrollbar = tb.Scrollbar(listbox, bootstyle="round")
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # 选中即复制选项
    copy_var = tk.BooleanVar()
    tb.Checkbutton(dict_frame, text="选中即复制", variable=copy_var, bootstyle="info-round-toggle").pack(pady=3)

    def on_listbox_select(event):
        """当选中列表项时，如果启用了'选中即复制'，则复制选中项"""
        if copy_var.get():
            copy_selected(listbox, edit_window)

    # 绑定选中事件
    listbox.bind("<<ListboxSelect>>", on_listbox_select)

    # 设置右键菜单
    setup_context_menu(listbox, edit_window)
    # 初始更新词典视图
    update_dict_view(listbox, word_type)

    # 计算编辑词典窗口位置
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    window_width = 800
    window_height = 600
    x = root_x + (root_width - window_width) // 2
    y = root_y + (root_height - window_height) // 2
    edit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")


def select_path(path_entry):
    """选择词库路径"""
    file_path = filedialog.askopenfilename(title="选择默认词典文件", filetypes=[("JSON 文件", "*.json")])
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)


def save_settings(path_entry, settings_window):
    """保存设置"""
    global current_dict_path
    new_path = path_entry.get().strip()
    if new_path and os.path.exists(new_path):
        try:
            with open(new_path, "r", encoding="utf-8") as f:
                global custom_dict
                custom_dict = json.load(f)
            current_dict_path = new_path
            # 保存配置
            config = {'dict_path': current_dict_path}
            with open(get_config_path(), "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            show_message(settings_window, "成功", "默认词库路径已更新")
            settings_window.destroy()
        except Exception as e:
            show_message(settings_window, "错误", f"加载新词典时发生错误: {e}", "error")
    else:
        show_message(settings_window, "警告", "请输入有效的 JSON 文件路径", "warning")


def open_settings_window():
    """打开设置窗口"""
    settings_window = tb.Toplevel(root)
    settings_window.title("设置")
    set_window_icon(settings_window)

    settings_frame = tb.Frame(settings_window, padding=10)
    settings_frame.pack(fill=BOTH, expand=True)

    tb.Label(settings_frame, text="默认词库路径", bootstyle="inverse-light").pack(anchor="w")
    path_entry = tb.Entry(settings_frame, font=("Segoe UI", 12))
    path_entry.insert(0, current_dict_path)
    path_entry.pack(fill=X, pady=5)

    button_frame = tb.Frame(settings_frame)
    button_frame.pack(fill=X, pady=10)

    tb.Button(button_frame, text="选择文件", bootstyle="secondary",
              command=lambda: select_path(path_entry)).pack(side=LEFT, padx=5)
    tb.Button(button_frame, text="保存设置", bootstyle="success",
              command=lambda: save_settings(path_entry, settings_window)).pack(side=RIGHT, padx=5)

    # 计算设置窗口位置
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    window_width = 500
    window_height = 150
    x = root_x + (root_width - window_width) // 2
    y = root_y + (root_height - window_height) // 2
    settings_window.geometry(f"{window_width}x{window_height}+{x}+{y}")


def open_about_window():
    """打开关于页面"""
    about_window = tb.Toplevel(root)
    about_window.title("关于")
    set_window_icon(about_window)

    about_frame = tb.Frame(about_window, padding=10)
    about_frame.pack(fill=BOTH, expand=True)

    tb.Label(about_frame, text="日文汉字 - 假名/罗马音转换工具", font=("Segoe UI", 16, "bold")).pack(pady=10)
    tb.Label(about_frame, text="这是一款用于将日文汉字转换为假名和罗马音的工具。", font=("Segoe UI", 12)).pack(pady=5)
    tb.Label(about_frame, text="支持自定义词典。", font=("Segoe UI", 12)).pack(pady=5)

    # 加载图片
    try:
        image = Image.open(resource_path("hantokana.png"))  # 替换为实际图片路径
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(about_frame, image=photo)
        image_label.image = photo
        image_label.pack(pady=10)
    except Exception as e:
        print(f"加载图片失败: {str(e)}")

    tb.Label(about_frame, text="版本: 0.2", font=("Segoe UI", 12)).pack(pady=5)
    tb.Label(about_frame, text="https://github.com/kanocyann/hantokana", font=("Segoe UI", 12)).pack(pady=5)

    # 计算关于窗口位置
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    about_frame.update_idletasks()
    window_width = about_frame.winfo_reqwidth() + 20
    window_height = about_frame.winfo_reqheight() + 20
    x = root_x + (root_width - window_width) // 2
    y = root_y + (root_height - window_height) // 2
    about_window.geometry(f"{window_width}x{window_height}+{x}+{y}")


def get_kana(surface):
    """用 pyKakasi 将词转换为平假名"""
    kana = ""
    for token in conv.convert(surface):
        kana += token['hira']
    return kana


def convert_text(text_input, text_output_text, use_hira, use_kata, use_roma):
    """执行日语文本转换：显示平假名、片假名和罗马音"""
    global tagger, conv
    if conv is None:
        conv = init_kks()
    if tagger is None:
        tagger = init_tagger()

    raw = text_input.get("1.0", tk.END).strip()
    if not raw:
        update_output(text_output_text, "请输入日文文本。")
        return
    if not (use_hira.get() or use_kata.get() or use_roma.get()):
        show_message(root, "警告", "请选择至少一个转换方式", "warning")
        return

    result = ""
    try:
        # 先进行正常分词
        words = tagger(raw)
        i = 0
        while i < len(words):
            # 尝试合并复合词
            for j in range(len(words), i, -1):
                combined = ''.join([w.surface for w in words[i:j]])
                if combined in custom_dict["compound_words"]:
                    word = combined
                    i = j
                    break
            else:
                word = words[i].surface
                i += 1

            # 优先使用自定义词典
            readings = custom_dict["normal_words"].get(word) or custom_dict["compound_words"].get(word)
            if not readings:
                # 使用pykakasi转换
                converted = conv.convert(word)
                readings = [item['hira'] for item in converted]

            for reading in readings:
                hira = jaconv.kata2hira(reading)
                line = f"[{word}]"
                if use_hira.get():
                    line += f" → [{hira}]"
                if use_kata.get():
                    kata = jaconv.hira2kata(hira)
                    line += f" → [{kata}]"
                if use_roma.get():
                    roma_item = conv.convert(reading)[0]
                    roma = roma_item['hepburn']
                    line += f" → [{roma}]"
                result += line + "\n"
        update_output(text_output_text, result.strip())
    except Exception as e:
        show_message(root, "错误", str(e), "error")


def update_output(text_output_text, text):
    """更新输出区域"""
    text_output_text.text.configure(state="normal")
    text_output_text.text.delete("1.0", tk.END)
    text_output_text.text.insert(tk.END, text)
    text_output_text.text.configure(state="disabled")


def copy_result(text_output_text, root):
    """复制转换结果"""
    root.clipboard_clear()
    root.clipboard_append(text_output_text.text.get("1.0", tk.END).strip())
    show_message(root, "成功", "已复制到剪贴板")


def confirm_exit():
    """退出确认提示"""
    confirm_dialog = tb.Toplevel(root)
    confirm_dialog.title("确认退出")
    set_window_icon(confirm_dialog)

    frame = tb.Frame(confirm_dialog, padding=10)
    frame.pack(fill=BOTH, expand=True)

    tb.Label(frame, text="⚠", font=("Segoe UI", 24), bootstyle="warning").pack(pady=10)
    tb.Label(frame, text="确定要退出应用程序吗？", font=("Segoe UI", 12)).pack(pady=5)

    button_frame = tb.Frame(frame)
    button_frame.pack(pady=10)

    def do_exit():
        confirm_dialog.destroy()
        root.destroy()

    tb.Button(button_frame, text="确定", bootstyle="danger", command=do_exit).pack(side=LEFT, padx=10)
    tb.Button(button_frame, text="取消", bootstyle="secondary", command=confirm_dialog.destroy).pack(side=RIGHT,
                                                                                                     padx=10)

    # 计算确认退出窗口位置
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    dialog_width = 340
    dialog_height = 200
    x = root_x + (root_width - dialog_width) // 2
    y = root_y + (root_height - dialog_height) // 2
    confirm_dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")


# 加载配置和字典
load_config()
load_custom_dict()

# 主窗口设置
root = tb.Window(themename="minty")
root.title("日文汉字-假名/罗马音 转换工具")
# 设置主窗口初始大小为 850x700
window_width = 850
window_height = 700

# 获取屏幕尺寸
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算主窗口位置
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 直接设置主窗口位置
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

set_window_icon(root)

# 点击“X”时弹出退出确认提示
root.protocol("WM_DELETE_WINDOW", confirm_exit)

style = tb.Style()
# 应用词典编辑页面滚动条样式
style.configure("Vertical.TScrollbar", bootstyle="round", width=8)
style.configure("Horizontal.TScrollbar", bootstyle="round", width=8)

main_frame = tb.Frame(root, padding=10)
main_frame.pack(fill=BOTH, expand=True)

# 菜单
menubar = Menu(root)
root.config(menu=menubar)
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="文件", menu=file_menu)
settings_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="设置", menu=settings_menu)
help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="帮助", menu=help_menu)

# 添加菜单项
file_menu.add_command(label="导入词典", command=load_dict)
file_menu.add_command(label="编辑普通词词典", command=lambda: open_edit_dict_window("normal_words"))
file_menu.add_command(label="编辑复合词词典", command=lambda: open_edit_dict_window("compound_words"))
settings_menu.add_command(label="设置默认词库路径", command=open_settings_window)
file_menu.add_command(label="退出", command=confirm_exit)
help_menu.add_command(label="关于", command=open_about_window)

# 主界面输入区域
tb.Label(main_frame, text="输入日文文本", font=("Segoe UI", 12, "bold")).pack(anchor="w")
text_input = ScrolledText(main_frame, height=6, font=("Segoe UI", 10), wrap="word")
text_input.pack(fill=BOTH, expand=False, pady=5)

# 转换选项
tb.Label(main_frame, text="转换方式", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 0))
mode_frame = tb.Frame(main_frame)
mode_frame.pack(fill=X, pady=5)

use_hira = tk.BooleanVar(value=True)
use_kata = tk.BooleanVar(value=True)
use_roma = tk.BooleanVar(value=True)

tb.Checkbutton(mode_frame, text="平假名", variable=use_hira).pack(side=LEFT, padx=10)
tb.Checkbutton(mode_frame, text="片假名", variable=use_kata).pack(side=LEFT, padx=10)
tb.Checkbutton(mode_frame, text="罗马音", variable=use_roma).pack(side=LEFT, padx=10)

# 转换按钮
convert_button = tb.Button(main_frame, text="开始转换", bootstyle=PRIMARY,
                           command=lambda: convert_text(text_input, text_output_text, use_hira, use_kata, use_roma))
convert_button.pack(pady=10)

# 输出区域
tb.Label(main_frame, text="转换结果", font=("Segoe UI", 12, "bold")).pack(anchor="w")
text_output_text = ScrolledText(main_frame, height=8, font=("Segoe UI", 10), wrap="word")
text_output_text.pack(fill=BOTH, expand=True, pady=5)
text_output_text.text.configure(state="disabled")

# 复制按钮
copy_button = tb.Button(main_frame, text="复制结果", bootstyle="secondary",
                        command=lambda: copy_result(text_output_text, root))
copy_button.pack(pady=10)

# 运行主循环
root.mainloop()
