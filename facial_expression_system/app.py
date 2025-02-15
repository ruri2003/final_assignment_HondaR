#上で画像を開く
#左コントロールで決定
#escでキャンセル
#下で送信
#右で投稿
#ｑで終了

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

# ラベルを表示する関数
"""def show_input_label(text, font=("Arial", 24)):
    global input_label
    if input_label is not None:
        input_label.pack_forget()  # 以前のラベルを削除
    input_label = tk.Label(root, text=text, font=font)
    input_label.pack()
"""

def show_input_label(text, font=("Arial", 24), x=0, y=0, width=None, height=None):
    global input_label
    if input_label is not None:
        input_label.place_forget()  # 以前のラベルを削除

    input_label = tk.Label(root, text=text, font=font)
    
    # x, y 位置指定と、オプションで幅と高さを指定
    input_label.place(x=x, y=y, anchor='nw', width=width, height=height)  # nw は左上を基準に配置


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
    img.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img

# キャンセル・決定ボタンの画面を表示する関数
def show_cancel_decide_screen():
    show_input_label("決定 : ←キー、キャンセル : escキー", font=("Arial", 24), x=300, y=50, width=700, height=50)
    open_button.place_forget()
    cancel_button.place(x=300, y=600)
    decide_button.place(x=700, y=600)

# 最初の画面に戻る関数
def back_to_start():
    #print("aaa")
    result_text.delete(1.0, tk.END)  # テキスト内容のみ削除
    image_label.config(image='')  # 画像を消す（ラベルは表示のまま）
    cancel_button.place_forget()  # キャンセルボタンを非表示
    decide_button.place_forget()  # 決定ボタンを非表示
    #yes_button.place_forget()  # yesボタンを非表示
    #no_button.place_forget()  # noボタンを非表示
    appload_button.place_forget()  # 投稿ボタンを非表示
    open_button.place(x=500, y=600)  # 画像選択ボタンは表示のまま
    show_input_label("画像選択 : ↑キー", font=("Arial", 24), x=380, y=50, width=500, height=50)


# 決定ボタンが押されたときの関数
def on_decide():

    global image_path, entry_field,input_label
    caption = entry_field.get()  # 入力されたテキストを取得
    subprocess.run(['python', 'C:/Users/Honda/.vscode/facial_expression_system/test_requests.py', image_path, caption])  # キャプションを渡す
    end_appload()
    
# 投稿が終了したときの関数
def end_appload():
    global input_label
    image_label.place_forget()
    result_text.place_forget()

    if input_label is not None:
        input_label.pack_forget()

    #fin = tk.Label(root, text="投稿が完了しました", font=("Arial", 24))
    #fin.pack()
    show_input_label("投稿が完了しました", font=("Arial", 24), x=290, y=50, width=700, height=50)
    entry_field.place_forget()
    appload_button.place_forget()



def text_page():
    global multiple, entry_field, submit_button  # 変数をグローバル宣言

    # ラベルを表示
    show_input_label("コメントの入力をしてください 送信 : ↓キー", font=("Arial", 24), x=340, y=50, width=700, height=50)
    #show_input_label("送信 : ↓キー", font=("Arial", 24), x=350, y=50, width=700, height=50)

    # エントリフィールドの表示位置を調整
    entry_field = tk.Entry(root, width=40, font=("Arial", 24))
    entry_field.place(x=360, y=100, width=330, height=60)

    # 送信ボタンの位置を調整
    submit_button.place(x=500, y=600)

    # 他のボタンを非表示にする
    if multiple is not None:
        multiple.pack_forget()
    cancel_button.place_forget()
    decide_button.place_forget()
    appload_button.place_forget()



def submit_text(): 
    global submit_button, appload_button  # ボタンのグローバル変数を宣言

    # 入力されたテキストを取得
    input_text = entry_field.get()
    
    # テキストウィジェットをクリア
    result_text.delete(1.0, tk.END)
    
    # タグを設定してフォントサイズを変更
    result_text.tag_configure("big", font=("Helvetica", 32))  # フォントとサイズを設定
    
    # テキストを挿入し、"big"タグを適用
    result_text.insert(tk.END, f"入力されたコメント: {input_text}", "big")

    # 送信ボタンを非表示にし、投稿ボタンを表示する
    submit_button.place_forget()  # 送信ボタンを削除
    appload_button.place(x=500, y=600)  # 投稿ボタンを表示
    show_input_label("投稿 : Enterキー", font=("Arial", 24), x=290, y=50, width=700, height=50)



# キーイベントの設定
def bind_keys():
    root.bind('<Escape>', lambda event: back_to_start())
    root.bind('<Up>', lambda event: on_open_image())
    root.bind('<Left>', lambda event: text_page())
    root.bind('<Down>', lambda event: submit_text())
    root.bind('<Return>', lambda event: on_decide())

# Tkinterウィンドウのセットアップ
root = tk.Tk()
root.attributes('-fullscreen', True)

# 'q'キーが押されたらウィンドウを閉じる
root.bind('<q>', lambda event: root.destroy())

# キーのバインド
bind_keys()

# 画像を表示するラベルの作成
image_label = tk.Label(root)
image_label.place(x=50, y=100)

# 画像を開くためのボタン
open_button = tk.Button(root, text="画像の選択", command=on_open_image, width=20, height=3, font=("Arial", 16))
open_button.place(x=500, y=600)
show_input_label("画像選択 : ↑キー", font=("Arial", 24), x=380, y=50, width=500, height=50)

# キャンセルボタンの作成（最初は非表示）
cancel_button = tk.Button(root, text="キャンセル", command=back_to_start, width=20, height=3, font=("Arial", 16))

# 決定ボタンの作成（最初は非表示）
decide_button = tk.Button(root, text="決定", command=text_page, width=20, height=3, font=("Arial", 16))

#送信ボタンの作成(最初は非表示)
submit_button = tk.Button(root, text="送信", command=submit_text, width=20, height=3, font=("Arial", 16))

# 投稿ボタンの作成(最初は非表示)
appload_button = tk.Button(root, text="投稿", command=on_decide, width=20, height=3, font=("Arial", 16))

# 結果を表示するテキストウィジェットの作成
result_text = tk.Text(root, height=20, width=50, font=("Arial", 14)) #文字の大きさ変える？？
result_text.place(x=700, y=100)

# Tkinterのイベントループを開始
root.mainloop()
