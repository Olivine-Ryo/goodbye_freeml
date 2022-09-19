import time
import traceback
import chromedriver_binary
import re
import sys
import os
import copy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

mail= input('Input your ID >>>')
password= input('Input your Pass >>>')
group_name = "" #グループ名を指定
page_max = 32
dldir_name = 'archive_data'  # 保存先フォルダ名
dldir_path = Path(dldir_name)
dldir_path.mkdir(exist_ok=True)  # 存在していてもOKとする（エラーで止めない）
download_dir = str(dldir_path.resolve())  # 絶対パス

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"download.default_directory": download_dir,"plugins.always_open_pdf_externally": True})


#options.add_argument("--headless") # ヘッドレスモードで実行する場合
driver = webdriver.Chrome(options=options)

# ログイン処理

driver.get("https://www.freeml.com/ep.umzx/grid/General/node/SpLoginFront/")
form_mail = driver.find_element_by_class_name("input_style")
form_mail.send_keys(mail)
form_pass = driver.find_element_by_id("password")
form_pass.send_keys(password)
time.sleep(2)
login_button = driver.find_element_by_class_name("login_bt2")
login_button.click()


#ダウンロードリンクの取得

filename_list=[]
for j in range(1, page_max + 1):
    url_page="https://www.freeml.com/" + group_name + "/files/" + str(j)
    driver.get(url_page)
    
    text=re.findall(group_name + '/file/[0-9]{5,6}">\n\t\t\t\t\t\t\t\t\t\t<h4>.*</h4>', driver.page_source)
    
    url_list=[]
    for i in range(0,len(text)): 
        url_list.append(re.search('[0-9]{5,6}',text[i]).group(0))
        filename_list.append(re.search(r'<h4>(.+)(</h4>)',text[i]).group(1)) 

    for url in url_list:
        url_download ='https://www.freeml.com/pso-all/file/' + url
        try:
            driver.get(url_download)
            url_downloadlink ='https://www.freeml.com/' + re.findall('ep.umzx/grid/MLC/node/MlcFileDownloadFront/param/.*">', driver.page_source)[0][:-2]
            driver.get(url_downloadlink)
        except:
            traceback.print_exc()
        time.sleep(0.25)
driver.quit()


# 文字化けしたファイル名の修正

count = len(filename_list)
os.chdir(dldir_name)
files = os.listdir(".")
files.sort(key=os.path.getmtime, reverse=False)
for (i,filename) in enumerate(files): 
    newname = str(count).zfill(3) + '-' + re.sub('[/,?,<,>,",:,|,\,*]', '-', filename_list[i])
    os.rename(filename,newname)  
    count -= 1
os.chdir("..")


