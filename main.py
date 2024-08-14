import json
import os
import datetime

import pandas as pd

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
def main(total_dell):
    file = 'info.xlsx'
    df = pd.read_excel(file).fillna(0)
    print(df)
    data_json_path = './data/images.json'
    with open(data_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(data)
    for index, row in df.iterrows():
        delled = row['delled']
        needDell = 0
        if total_dell == 0:
            if delled != 1:
                needDell = 1
        else:
            needDell = 1
        if needDell == 1:
            if row['refreshTime'] == 0:
                time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row['refreshTime'] = time_str
                df.loc[index,'refreshTime'] = time_str

            data_row =  {
                            "title":row['title'],
                            "desc":row['desc'],
                            "tags":row['tags'].split(","),
                            "picPath":row['picPath'],
                            "urlLink":row['urlLink'],
                            "refreshTime":row['refreshTime'],
                            "hot":row['hot']
                        }
            data.append(data_row)

            urlLink = row['urlLink']
            path_html = f'./pages/{urlLink}'
            # if not os.path.exists(path_html):
            if True:
                content = creatHtml(row)
                # print(content)
                with open(path_html, 'w', encoding='utf-8') as f:
                    f.write(content)
            df.loc[index,'delled'] = 1
    with open(data_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(df)

if __name__ == '__main__':
    total_dell = 0
    main(total_dell)