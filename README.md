# 粽子目標偵測

本專案使用 [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) 訓練粽子目標偵測模型。目前模型只有一個類別：

| 類別編號 | 類別名稱 |
| --- | --- |
| 0 | `zongzi`（粽子） |

## 專案結構

```text
.
├── datasets/
│   ├── data.yaml
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   └── val/
│       ├── images/
│       └── labels/
├── runs/detect/zongzi_detector/
│   └── weights/
│       ├── best.pt
│       └── last.pt
├── train.py
├── test_and_export.py
├── test_image.jpg
└── yolo11n.pt
```

## 環境需求

- Windows
- Python 3.13
- NVIDIA GPU 與 CUDA（訓練腳本預設使用 `device=0`）
- Ultralytics、PyTorch、OpenCV 等套件

專案中已包含虛擬環境 `ai_hw_env`。若要啟用此環境，可在 PowerShell 執行：

```powershell
.\ai_hw_env\Scripts\Activate.ps1
```

也可以不啟用環境，直接使用其中的 Python：

```powershell
.\ai_hw_env\Scripts\python.exe --version
```

## 資料集格式

資料集設定檔為 [`datasets/data.yaml`](datasets/data.yaml)：

```yaml
train: ./datasets/train/images
val: ./datasets/val/images
nc: 1
names: ['zongzi']
```

訓練資料與驗證資料分別放在以下目錄：

```text
datasets/
├── train/
│   ├── images/    # 訓練圖片
│   └── labels/    # 訓練標註
└── val/
    ├── images/    # 驗證圖片
    └── labels/    # 驗證標註
```

每張圖片都應該有一個放在 `labels` 目錄、且檔名相同的 `.txt` 標註檔。YOLO 標註格式如下：

```text
class_id x_center y_center width height
```

所有座標與寬高都必須正規化為 `0` 到 `1` 之間。由於本專案只有一個類別，`class_id` 必須設定為 `0`。

## 訓練模型

訓練程式為 [`train.py`](train.py)，目前使用以下設定：

- 預訓練模型：`yolo11n.pt`
- 訓練回合數：100
- 圖片尺寸：`640`
- 批次大小：`16`
- GPU 裝置：`0`
- DataLoader 執行緒數：`0`
- 訓練名稱：`zongzi_detector`

請先確認目前位於專案根目錄，再執行：

```powershell
.\ai_hw_env\Scripts\python.exe train.py
```

訓練結果會儲存於：

```text
runs/detect/zongzi_detector/
```

其中：

- `weights/best.pt`：驗證結果最佳的模型權重
- `weights/last.pt`：最後一個訓練回合的模型權重

## 測試模型與匯出 ONNX

測試與匯出程式為 [`test_and_export.py`](test_and_export.py)，會依序執行以下工作：

1. 載入 `runs/detect/zongzi_detector/weights/best.pt`。
2. 使用 [`test_image.jpg`](test_image.jpg) 進行目標偵測。
3. 將繪製偵測框的結果儲存至 `runs/detect/predict/`。
4. 將模型匯出為 ONNX 格式。

執行方式：

```powershell
.\ai_hw_env\Scripts\python.exe test_and_export.py
```

程式目前將信心度門檻設定為 `0.5`。如果尚未完成訓練，或找不到 `best.pt`，請先完成訓練，或將程式中的模型路徑改成實際存在的 `.pt` 檔案。

## 使用 Ultralytics 命令列

也可以直接使用 Ultralytics 命令列進行推論：

```powershell
.\ai_hw_env\Scripts\yolo.exe predict `
    model=runs/detect/zongzi_detector/weights/best.pt `
    source=test_image.jpg `
    conf=0.5 `
    save=True
```

將模型匯出為 ONNX：

```powershell
.\ai_hw_env\Scripts\yolo.exe export `
    model=runs/detect/zongzi_detector/weights/best.pt `
    format=onnx
```

## 圖片重新命名工具

[`rename.py`](rename.py) 可以將資料夾中的圖片依序重新命名，例如：

```text
zongzi_0001.webp
zongzi_0002.webp
zongzi_0003.webp
```

使用前請確認程式中的 `folder_path` 指向正確的圖片資料夾，並建議先備份資料集。重新命名圖片時，也要確保對應的標註檔案名稱同步更新，否則圖片與標註可能無法配對。

## 模型檔案

目前專案包含以下模型檔案：

- [`yolo11n.pt`](yolo11n.pt)：YOLO11 nano 預訓練模型
- [`runs/detect/zongzi_detector/weights/best.pt`](runs/detect/zongzi_detector/weights/best.pt)：訓練後的最佳模型
- [`runs/detect/zongzi_detector/weights/last.pt`](runs/detect/zongzi_detector/weights/last.pt)：最後一個訓練回合的模型

模型檔案通常較大。若要將專案提交至 Git 儲存庫，建議使用 Git LFS 或其他模型檔案儲存服務。

## 常見問題

### 找不到 `zongzi.yaml`

請將 [`train.py`](train.py) 中的：

```python
data='zongzi.yaml'
```

改為：

```python
data='datasets/data.yaml'
```

### Windows 下 DataLoader 發生錯誤

請將訓練參數中的 `workers` 設定為 `0`，並確認訓練程式使用以下入口寫法：

```python
if __name__ == '__main__':
    main()
```

### 沒有可用的 GPU

如果電腦沒有可用的 CUDA GPU，可以將 [`train.py`](train.py) 中的：

```python
device=0
```

改為：

```python
device='cpu'
```

CPU 訓練通常會比 GPU 慢很多。
