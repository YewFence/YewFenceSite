import os
from PIL import Image

# ----- 配置 -----

SOURCE_DIR = 'docs/images'         # 原始图片文件夹
OUTPUT_DIR = 'docs/images/webp_output'    # 存放的文件夹
QUALITY = 80                  # 有损压缩的质量 (1-100)
# ------------------

# 1. 确保输出文件夹存在
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"开始转换: '{SOURCE_DIR}' -> '{OUTPUT_DIR}'")

# 2. 遍历源文件夹中的所有文件
for filename in os.listdir(SOURCE_DIR):
    # 构造完整的文件路径
    file_path = os.path.join(SOURCE_DIR, filename)
    
    # 检查是否是文件，以及是否是我们要的图片格式
    if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        
        # 构造输出文件名
        # 'image.png' -> 'image.webp'
        new_filename = os.path.splitext(filename)[0] + '.webp'
        output_path = os.path.join(OUTPUT_DIR, new_filename)

        try:
            # 使用 'with' 语句打开图片，更安全
            with Image.open(file_path) as img:
                
                # 3. 根据原始格式决定压缩策略
                if filename.lower().endswith('.png'):
                    # PNGs (logo, 截图) -> 使用无损
                    img.save(output_path, format='WebP', lossless=True)
                    print(f"[无损] {filename} -> {new_filename}")
                else:
                    # JPGs (照片) -> 使用有损质量
                    img.save(output_path, format='WebP', quality=QUALITY)
                    print(f"[质量 {QUALITY}] {filename} -> {new_filename}")

        except Exception as e:
            print(f"转换失败 {filename}: {e}")

print("--- 批量转换完成! ---")