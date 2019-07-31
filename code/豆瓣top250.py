import requests
from bs4 import BeautifulSoup

import os
import shutil

def geturl(url):
    try:
        d_data=requests.get(url)
        d_data.raise_for_status()
        d_data.encoding=d_data.apparent_encoding
        return d_data.text
    except:
        print("get error")

def parse_web(top,html):
    try:
        soup=BeautifulSoup(html,"lxml")
        titles=soup.select("div.hd>a")
        rates=soup.select('span.rating_num')
        imgs=soup.select('img[width="100"]')

        for title,rate,img in zip(titles,rates,imgs):
            data={
                'title':list(title.stripped_strings),#获取多个元素值stripped_strings
                'rate':rate.get_text(),#beautifulsoup内部才有text这个属性，只供内部使用 –> 如果你想要用text值，应该调用对应的get_text()
                'img':img.get('src'),
            }
            top=top+1
            filename=str(top)+"."+data['title'][0]+' '+data['rate']+'分.jpg'
            pic=requests.get(data['img'])
            with open("pic\\"+filename,"wb")as photo:
                photo.write(pic.content)
            print(pic)
            print(data)
    except:
        print("parse erorr")

def clean_file(path):
    shutil.rmtree(path)  # 能删除该文件夹和文件夹下所有文件
    os.mkdir(path)

# url="https://movie.douban.com/top250"
'''https://movie.douban.com/top250?start=25&filter='''
def main():
    top=0
    for url in ['https://movie.douban.com/top250?start=' + str(n) + '&filter=' for n in range(0, 250, 25)]:
        parse_web(top,geturl(url))
        top = top + 25

#clean_file("pic")
main()



