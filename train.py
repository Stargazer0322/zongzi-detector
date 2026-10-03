# coding=Big5
from ultralytics import YOLO

def main():
    # 1. 載入預訓練模型
    # 這裡使用 YOLOv8 的 nano 版本 (yolov8n.pt)，模型最小、訓練最快，適合跑作業。
    # 如果你想用最新的 YOLOv11，可以改成 'yolo11n.pt'
    model = YOLO('yolo11n.pt')

    # 2. 開始訓練
    print("? 開始訓練粽子偵測器...")
    results = model.train(
        data='datasets/data.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        device=0,
        name='zongzi_detector',
        plots=True,
        amp=False,     # 新增：關閉自動混合精度，避免顯示卡檢查卡死
        workers=0      # 新增：將資料載入執行緒設為 0，防止 Windows 多進程死鎖
    )
    print("? 訓練完成！")

if __name__ == '__main__':
    # 在 Windows 系統跑多執行緒訓練時，這行 if __name__ == '__main__': 是必備的
    main()