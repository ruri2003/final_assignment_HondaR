import argparse 
import os
import sys
from pathlib import Path
import cv2  # OpenCV for image handling
import torch
from collections import defaultdict  # クラスごとのカウントに使用

# YOLOv5関連のインポート
from utils.dataloaders import LoadImages, LoadStreams, LoadScreenshots
from utils.general import increment_path, check_img_size, scale_boxes, non_max_suppression
from models.common import DetectMultiBackend

# バウンディングボックス描画用の関数
def draw_bounding_box(image, box, label=None, color=(255, 0, 0), thickness=2):
    x1, y1, x2, y2 = map(int, box)  # 座標を整数にキャスト
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)  # バウンディングボックスを描画
    if label:
        # ラベルを表示
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, label, (x1, y1 - 10), font, 0.9, color, 2)

# クラスIDに基づいた色取得関数
def get_color(class_id):
    """
    Get a color based on the class ID.
    Args:
        class_id: The class ID of the object.
    Returns:
        A tuple representing the color (B, G, R).
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    return colors[class_id % len(colors)]

# バウンディングボックスをクロップして保存する関数
"""def save_cropped_box(image, box, save_path):
    
    Save a cropped portion of the image.
    Args:
        image: The original image.
        box: Coordinates of the bounding box [x1, y1, x2, y2].
        save_path: Path to save the cropped image.
    
    x1, y1, x2, y2 = map(int,box)
    cropped_image = image[y1:y2, x1:x2]
    success = cv2.imwrite(save_path, cropped_image)
    if success:
        print(f"Cropped image successfully saved to {save_path}")
    else:
        print(f"Failed to save cropped image to {save_path}")
"""
# YOLOv5の推論を実行するメイン関数
@torch.no_grad()
def run(
    weights=Path("yolov5s.pt"),  # モデルパス
    source=None,  # 画像パス
    imgsz=(640, 640),  # 推論サイズ (height, width)
    conf_thres=0.25,  # 信頼度閾値
    iou_thres=0.45,  # NMSのIOU閾値
    max_det=1000,  # 画像ごとの最大検出数
    device="",  # 使用するデバイス (cpu/cuda)
    save_dir="C:/Users/Honda/.vscode/yolov5-master/data_save/",  # 保存するディレクトリのパス
    save_img=True  # 画像の保存
):
    # 保存ディレクトリの存在確認・作成
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)  # ディレクトリがなければ作成
    
    # 画像が指定されているか確認
    if source is None:
        raise ValueError("Source (image_path) must be provided!")
    
    # モデルの読み込み
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DetectMultiBackend(weights, device=device)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # 画像サイズの確認

    # 画像の読み込み
    dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # クラスごとのカウント用辞書
    class_counts = defaultdict(int)

    # 推論の実行
    for path, img, im0s, vid_cap, s in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float()  # FP32推論
        img /= 255.0  # 0 - 255 to 0.0 - 1.0

        # バッチサイズの次元を追加 (C, H, W) -> (1, C, H, W)
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # 推論
        pred = model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False)

        # 検出結果の処理
        for i, det in enumerate(pred):
            im0 = im0s.copy()
            save_path = save_dir / "output.jpg"  # バウンディングボックスを描画した画像の保存パス

            if len(det):
                # スケーリング
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0.shape).round()

                # 各検出ボックスに対して描画と保存を行う
                for *box, conf, cls in det:
                    label = f"{names[int(cls)]} {conf:.2f}"
                    draw_bounding_box(im0, box, label, color=get_color(int(cls)))

                    # クロップされたボックスの保存
                    #cropped_save_path = save_dir / "cropped_image.jpg"
                    #save_cropped_box(im0, box, str(cropped_save_path))

                    # クラスごとのカウントを更新
                    class_counts[names[int(cls)]] += 1

            # 画像の保存
            if save_img:
                cv2.imwrite(str(save_path), im0)
                #print(f"Image with bounding boxes saved to {save_path}")

    # 検出クラスごとのカウントをプリント
    #print("\nDetection results:")
    for class_name, count in class_counts.items():
        print(f"{class_name}: {count}")

if __name__ == "__main__":
    #image_path = "C:/Users/Honda/.vscode/yolov5-master/data_pic/cat.jpg"  # 画像パス
    if len(sys.argv) < 2:
        print("画像のパスを指定してください。")
        sys.exit(1)
    image_path = sys.argv[1]  # コマンドラインから画像パスを取得検出された顔の数
    
    run(source=image_path)  # 推論の実行
