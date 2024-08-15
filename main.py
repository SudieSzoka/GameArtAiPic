import json
import os
import datetime

import pandas as pd
from PIL import Image

output_width, output_height = 300, 300
def resize_and_crop_image(input_image_path, output_width, output_height, output_path):
    # 打开原始图片
    with Image.open(input_image_path) as img:
        # 获取原始图片的宽度和高度
        original_width, original_height = img.size
        
        # 计算目标宽高比
        ratio = max(output_width/original_width, output_height/original_height)
        
        # 计算缩放后的尺寸
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # 缩放图片，保持原始宽高比
        img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # 计算裁剪的位置
        crop_width = output_width
        crop_height = output_height
        left = (new_width - crop_width) // 2
        top = (new_height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height
        
        # 裁剪图片
        img = img.crop((left, top, right, bottom))
        
        # 保存图片
        img.save(output_path)

template_path = './pages/template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()
def creatHtml(row):
    list_placeholder = ['{{picPath}}','{{tags}}','{{desc}}','{{refreshTime}}']
    list_replace = [row['picPath'],row['tags'],row['desc'],str(row['refreshTime'])]
    content = template
    for i in range(len(list_placeholder)):
        content = content.replace(list_placeholder[i],list_replace[i])
    return content

path_tags = './data/key.json'
def dellTags(tags,reWrite = 0):
    data = json.load(open(path_tags, 'r', encoding='utf-8'))
    for tag in tags:
        if tag not in data['keywords']:
            data['keywords'].append(tag)
    if reWrite == 1:
        data = {'keywords':tags}
    with open(path_tags, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
def main(total_dell,file):
    # file = 'info.xlsx'
    df = pd.read_excel(file).fillna(0)
    # print(df)
    data_json_path = './data/images.json'
    with open(data_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if total_dell == 1:
        data = []
    # print(data)
    tags_total = []
    for index, row in df.iterrows():
        try:
            delled = int(row['delled'])
        except:
            delled = 0
        needDell = 0
        
        if total_dell == 0:
            if delled != 1:
                needDell = 1
        else:
            needDell = 1
        if needDell == 1:
            if row['refreshTime'] == "" or row['refreshTime'] == 0 or row['refreshTime'] == 0.0:
                time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row['refreshTime'] = time_str
                df.loc[index,'refreshTime'] = time_str
            
            tags = row['tags'].split(",")
            if total_dell == 1:
                for t in tags:
                    if t not in tags_total:
                        tags_total.append(t)
            dellTags(tags)

            picPath = row['picPath']
            pic_origin = './pic/' + picPath
            output_name = 'small_' + picPath
            output_path = './pic/' + output_name
            resize_and_crop_image(pic_origin, output_width, output_height, output_path)
            data_row =  {
                            "title":row['title'],
                            "desc":row['desc'],
                            "tags":tags,
                            "picPath":row['picPath'],
                            "picSmall":output_name,
                            "urlLink":row['urlLink'],
                            "refreshTime":row['refreshTime'],
                            "hot":row['hot']
                        }
            data.append(data_row)
            data = [data_row] + data

            urlLink = row['urlLink']
            path_html = f'./pages/{urlLink}'
            needCreatHtml = False
            if total_dell:
                needCreatHtml = True
            else:
                if not os.path.exists(path_html):
                    needCreatHtml = True
            if needCreatHtml:
                content = creatHtml(row)
                # print(content)
                with open(path_html, 'w', encoding='utf-8') as f:
                    f.write(content)
            df.loc[index,'delled'] = 1
    with open(data_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # print(df)
    if total_dell == 1:
        dellTags(tags_total,1)
    df.to_excel(file, index=False)

if __name__ == '__main__':
    total_dell = 0
    dell_file = 'info_240816.xlsx'
    main(total_dell,dell_file)