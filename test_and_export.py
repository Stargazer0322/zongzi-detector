# coding=Big5
from ultralytics import YOLO

def main():
    # 1. 載入你剛剛訓練出來「最棒的」權重檔 (.pt)
    # 預設路徑會長這樣，請確認 runs 資料夾有產生
    model_path = 'runs/detect/zongzi_detector/weights/best.pt'
    model = YOLO(model_path)

    # 2. 測試預測
    print("? 正在測試圖片...")
    # conf=0.5 代表信心水準大於 50% 才畫框；save=True 會幫你把畫好框的圖存下來
    results = model.predict(source='test_image.jpg', conf=0.5, save=True)
    print("? 測試圖片已儲存，可以去 runs/detect/predict 裡面查看！")

    # 3. 匯出模型 (應付作業 PS1 加分項)
    print("? 正在匯出 ONNX 格式...")
    model.export(format='onnx')
    print("? 匯出完成！你可以把 best.pt 跟 best.onnx 一起包裝交作業了。")

if __name__ == '__main__':
    main()