import json
import os
import datetime

import pandas as pd
from PIL import Image

output_width, output_height = 300, 300
def resize_and_crop_image(input_image_path,output_path):
    # 打开原始图片
    with Image.open(input_image_path) as img:
        # 等比例缩放，不超过 output_width, output_height
        img.thumbnail((output_width, output_height))
        # 保存问webp格式
        img.save(output_path,'WEBP')

def main():
    # 删除pic文件夹下 small_ 开头的图片
    # pic_dir = './pic/'
    # for file in os.listdir(pic_dir):
    #     if file.startswith('small_'):
    #         os.remove(os.path.join(pic_dir, file))
    data_json = './data/images.json'
    with open(data_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        pic_origin = './pic/' + item['picPath']
        output_name = 'small_' + item['picPath'].replace('.png','.webp')
        output_path = './pic/' + output_name
        resize_and_crop_image(pic_origin, output_path)
        # 更新数据
        item['picSmall'] = output_name
        # item['refreshTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(data_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False,indent=4)


if __name__ == '__main__':
    main()