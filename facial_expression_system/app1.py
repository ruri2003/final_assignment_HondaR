import tkinter as tk  
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess

# グローバル変数として image_path や multiple を定義
image_path = None
multiple = None
input_label = None
entry_field = None  # Entry ウィジェットの変数

# main.pyスクリプトを実行し、画像パスを引数として渡す関数
def run_main_script(image_path):
    result = subprocess.run(['python', 'C:/Users/Honda/.vscode/facial_expression_system/main.py', image_path], capture_output=True, text=True)
    return result.stdout

# 画像を開くための関数
def on_open_image():
    global image_path
    file_path = filedialog.askopenfilename()
    if file_path:
        image_path = file_path
        load_image(file_path)
        output = run_main_script(file_path)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, output)
        show_cancel_decide_screen()

# 画像を表示する関数
def load_image(image_path):
    img = Image.open(image_path)
    
    # 元のサイズを取得
    original_size = img.size  # (幅, 高さ)
    
    # 新しいサイズを計算（1.5倍）
    new_size = (int(original_size[0] * 0.4), int(original_size[1] * 0.4))
    
    # 画像をリサイズ
    img = img.resize(new_size, Image.LANCZOS)  # 高品質なリサイズ
    
    # 画像をTkinterで表示可能な形式に変換
    img = ImageTk.PhotoImage(img)

    # 画像をラベルに設定
    image_label.config(image=img)
    image_label.image = img

# キャンセル・決定ボタンの画面を表示する関数
def show_cancel_decide_screen():
    open_button.place_forget()
    cancel_frame.place(x=300, y=600)
    decide_frame.place(x=700, y=600)

# 最初の画面に戻る関数
def back_to_start():
    result_text.delete(1.0, tk.END)
    image_label.config(image='')
    cancel_frame.place_forget()
    decide_frame.place_forget()
    yes_button.place_forget()
    no_button.place_forget()
    appload_button.place_forget()
    open_button.place(x=500, y=600)

# 決定ボタンが押されたときの関数
def on_decide():
    global image_path, entry_field
    caption = entry_field.get()  # 入力されたテキストを取得
    subprocess.run(['python', 'C:/Users/Honda/.vscode/test1/test_requests.py', image_path, caption])  # キャプションを渡す
    end_appload()

def end_appload():
    global input_label
    # 表示されているウィジェットやラベルをすべて非表示にする
    image_label.place_forget()
    result_text.place_forget()

    if input_label is not None:
        input_label.pack_forget()  # input_label を非表示に

    # 新しいメッセージを表示
    fin = tk.Label(root, text="投稿が完了しました", font=("Arial", 24))
    fin.pack()

# 複数枚画像選択する関数
def multiple_choice():
    global multiple
    multiple = tk.Label(root, text="複数枚画像を選択しますか", font=("Arial", 24))
    multiple.pack()
    yes_button.place(x=300, y=600)
    no_button.place(x=700, y=600)

# テキストの入力ページ
def text_page():
    global input_label, multiple, entry_field
    input_label = tk.Label(root, text="テキストの入力をしてください", font=("Arial", 24))
    input_label.pack()
    if multiple is not None:
        multiple.pack_forget()
    cancel_frame.place_forget()
    decide_frame.place_forget()
    yes_button.place_forget()
    no_button.place_forget()
    appload_button.place(x=500, y=600)

    # Entryフィールドの作成
    entry_field = tk.Entry(root, width=40, font=("Arial", 18))
    entry_field.pack(pady=10)

    submit_button = tk.Button(root, text="送信", command=submit_text, width=20, height=3, font=("Arial", 16))
    submit_button.pack(pady=10)

# テキストを送信する関数
def submit_text():
    input_text = entry_field.get()  # Entryフィールドから入力されたテキストを取得
    
    # result_textの内容をクリア
    result_text.delete(1.0, tk.END)
    
    # 新しいテキストを result_text に挿入
    result_text.insert(tk.END, f"入力されたテキスト: {input_text}")

# Tkinterウィンドウのセットアップ
root = tk.Tk()
root.attributes('-fullscreen', True)

# 'q'キーが押されたらウィンドウを閉じる
root.bind('<q>', lambda event: root.destroy())

# 画像を表示するラベルの作成
image_label = tk.Label(root)
image_label.place(x=20, y=0)

# 画像を開くためのボタン
open_button = tk.Button(root, text="画像の選択", command=on_open_image, width=20, height=3, font=("Arial", 16))
open_button.place(x=0, y=600)

# キャンセルボタンを黒枠で囲むためのフレーム
cancel_frame = tk.Frame(root, bg="black")
cancel_button = tk.Button(cancel_frame, text="キャンセル", command=back_to_start, width=15, height=2, font=("Arial", 35), bg="white", borderwidth=0)
cancel_button.pack(padx=2, pady=2)

# 決定ボタンを黒枠で囲むためのフレーム
decide_frame = tk.Frame(root, bg="black")
decide_button = tk.Button(decide_frame, text="決定", command=multiple_choice, width=15, height=2, font=("Arial", 35), bg="white", borderwidth=0)
decide_button.pack(padx=2, pady=2)
"""
open_button = tk.Button(root, text="キャンセル", command=on_open_image, width=20, height=3, font=("Arial", 26))
open_button.place(x=300, y=600)
open_button = tk.Button(root, text="決定", command=on_open_image, width=20, height=3, font=("Arial", 16))
open_button.place(x=700, y=600)
"""

# はいボタンの作成(最初は非表示)
yes_button = tk.Button(root, text="はい", command=back_to_start, width=20, height=3, font=("Arial", 16))

# いいえボタンの作成(最初は非表示)
no_button = tk.Button(root, text="いいえ", command=text_page, width=20, height=3, font=("Arial", 16))

# 投稿ボタンの作成(最初は非表示)
appload_button = tk.Button(root, text="投稿", command=on_decide, width=20, height=3, font=("Arial", 16))

# 結果を表示するテキストウィジェットの作成
result_text = tk.Text(root, height=16, width=43, font=("Arial", 23))
result_text.place(x=500, y=0)

# Tkinterのイベントループを開始
root.mainloop()
