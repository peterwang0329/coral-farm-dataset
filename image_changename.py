import os
import re

# 預設多個資料夾的絕對路徑列表
DIRECTORY_PATHS = [
    r"C:\\Users\\peter\\Desktop\\program\\spider\\train\\images\\valid\\Amphiprion_clarkii\\label",
]
# 定義映射字典，將舊名稱映射到新名稱
NAME_MAPPING = {
    "Amphiprion clarkii 雙帶小丑": "Amphiprion_clarkii",
    "Amphiprion frenatus 紅小丑": "Amphiprion_frenatus",
    "Amphiprion ocellaris 公子小丑": "Amphiprion_ocellaris",
    "Acropora hyacinthus 桌形軸孔珊瑚": "Acropora_hyacinthus",
    "Acropora pruinosa 灰葉軸孔珊瑚": "Acropora_pruinosa",
    "Euphyllia glabrescens 束型針葉珊瑚": "Euphyllia_glabrescens",
    "Fimbriaphyllia ancora 錨形紋葉珊瑚": "Fimbriaphyllia_ancora",
    "Galaxea astreata 星形棘杯珊瑚": "Galaxea_astreata",
    "Nephthea sp 穗軟珊瑚": "Nephthea_sp",
    "Pavona decussata 板葉雀屏珊瑚": "Pavona_decussata",
    "Porites lobata 團塊微孔珊瑚": "Porites_lobata",
    "Stylophora pistillata 萼形柱珊瑚": "Stylophora_pistillata",
    "Turbinaria reniformis 腎形盤珊瑚": "Turbinaria_reniformis"
}

def extract_number_and_name(filename):
    """從檔案名稱中提取編號和名稱"""
    # 使用正則表達式處理複雜格式 (例如 Amphiprion_clarkii_199_1_1)
    match = re.match(r'^(.*?)_(\d+)(?:_\d+)*$', filename)
    if match:
        name = match.group(1)
        number = match.group(2)
        return number, name
    
    # 嘗試舊格式（數字名稱.副檔名格式）
    match = re.match(r'^(\d+)(.+)$', filename)
    if match:
        number = match.group(1)
        name = match.group(2)
        return number, name
    
    return None, None

def rename_files():
    """重新命名多個資料夾中的所有檔案"""
    
    # 遍歷所有指定的目錄路徑
    for directory_path in DIRECTORY_PATHS:
        # 用於存儲已使用的新檔案名稱，避免重複
        used_new_names = set()
        
        # 檢查目錄是否存在
        if not os.path.exists(directory_path):
            print(f"錯誤：資料夾 '{directory_path}' 不存在。")
            continue
        
        print(f"\n處理資料夾: {directory_path}")
        
        # 遍歷資料夾中的所有檔案
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # 檢查是否為檔案
            if os.path.isfile(file_path):
                # 獲取檔案名稱和擴展名
                base_name, ext = os.path.splitext(filename)
                
                # 檢查檔案是否已經符合我們的命名格式 (例如 Amphiprion_clarkii_8.jpg)
                folder_name = os.path.basename(directory_path)
                if base_name.startswith(folder_name) and re.match(r'^[^_]+_[^_]+_\d+$', base_name):
                    print(f"檔案 '{filename}' 已經符合命名格式，跳過處理。")
                    continue
                
                # 提取編號和舊名稱
                number, old_name = extract_number_and_name(base_name)
                
                if number is not None and old_name is not None:
                    # 獲取新名稱，如果映射中沒有則保持舊名稱
                    new_name_base = NAME_MAPPING.get(old_name, old_name)
                    
                    # 建立新檔案名稱
                    new_name = f"{new_name_base}_{number}{ext}"
                    new_path = os.path.join(directory_path, new_name)
                    
                    # 如果新名稱和當前名稱相同，則跳過
                    if new_name == filename:
                        print(f"檔案 '{filename}' 已經符合命名格式，跳過處理。")
                        continue
                    
                    # 檢查新檔案名稱是否已存在
                    counter = 1
                    while new_name in used_new_names or os.path.exists(new_path):
                        # 如果已存在，在檔案名後加上計數器
                        new_name = f"{new_name_base}_{number}_{counter}{ext}"
                        new_path = os.path.join(directory_path, new_name)
                        counter += 1
                    
                    # 記錄新檔案名稱
                    used_new_names.add(new_name)
                    
                    # 重新命名檔案
                    os.rename(file_path, new_path)
                    print(f"已重新命名: {filename} -> {new_name}")
                else:
                    print(f"無法從檔案名稱中提取編號和名稱: {filename}")
        
        print(f"資料夾 '{directory_path}' 處理完成！")
    
    print("\n所有資料夾的檔案重新命名完成！")

if __name__ == "__main__":
    rename_files()
