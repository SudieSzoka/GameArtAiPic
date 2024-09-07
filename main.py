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
        print('删除所有数据，重新开始')
    old_len = len(data)
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
            output_name = 'small_' + picPath.replace('.png','.webp')
            output_path = './pic/' + output_name
            resize_and_crop_image(pic_origin, output_path)
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
            # data.append(data_row)
            data = [data_row] + data

            urlLink = row['urlLink']
            path_html = f'./pages/{urlLink}'

            if True:
                content = creatHtml(row)
                # print(content)
                with open(path_html, 'w', encoding='utf-8') as f:
                    f.write(content)
            df.loc[index,'delled'] = 1
    new_len = len(data)
    print(f'数据新增:{new_len - old_len}条')
    with open(data_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # print(df)
    if total_dell == 1:
        dellTags(tags_total,1)
    df.to_excel(file, index=False)

if __name__ == '__main__':
    total_dell = 0
    dell_file = 'delled.xlsx'
    main(total_dell,dell_file)