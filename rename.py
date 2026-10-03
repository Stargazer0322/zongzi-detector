# coding=Big5
import os

# 1. 設定你的圖片資料夾路徑 (請替換成截圖中上方網址列的實際路徑)
# 路徑前面的 r 代表 raw string，可以避免 Windows 路徑的反斜線 \ 產生跳脫字元錯誤
folder_path = r"D:\code\hw2\datasets\train\images"
prefix = "zongzi_"

# 2. 取得資料夾內所有檔案，並過濾出實體檔案 (排除可能存在的子資料夾)
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# 3. 針對每個檔案進行重新命名
for index, filename in enumerate(files):
    # os.path.splitext 會將檔名拆成 [主檔名, 副檔名]
    # 例如 "10028.webp" 會變成 ["10028", ".webp"]，我們取 [1] 也就是 ".webp"
    file_extension = os.path.splitext(filename)[1]
    
    # 4. 組合出新的檔名
    # (index + 1):04d 代表將數字格式化為 4 位數，不足補零。例如 1 會變成 0001
    new_name = f"{prefix}{(index + 1):04d}{file_extension}"
    
    # 5. 組合出完整的舊路徑與新路徑
    old_file_path = os.path.join(folder_path, filename)
    new_file_path = os.path.join(folder_path, new_name)
    
    # 6. 執行重新命名動作
    os.rename(old_file_path, new_file_path)

print(f"? 成功重新命名 {len(files)} 個檔案！")