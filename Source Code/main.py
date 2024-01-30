import json
from selenium import webdriver
from time import sleep
import json
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import re
import shutil
import pyautogui
import pyperclip
import requests

##### google driver #####

# 讀取檔案
with open('env.json') as file:
    env = json.load(file)

# 提取 cookie_value 和 chromedriver_path 的值
PHPSESSID_COOKIE = env['cookie']
DRIVER_PATH = env['driver_path']
DOWNLOAD_PATH = env['download_path']

history_path =  'https://eeclass.nthu.edu.tw/dashboard/historyCourse'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') #最大化視窗
options.add_experimental_option("detach", True)

####### 開啟畫面 #######

driver = webdriver.Chrome(DRIVER_PATH,options=options)
driver.get(history_path)
driver.add_cookie(PHPSESSID_COOKIE)
driver.refresh()

#######################

## global sleep time ##
sleep_time = 0.5
#######################

def chinese_string(original_string):
    return re.sub("[^\u4e00-\u9fa5]", "", original_string) 

def format_string(text):
    symbols = ['\\', '/', ':', '*', '?', '"', '<', '>','|','-',' ']
    for symbol in symbols:
        text = text.replace(symbol, '_')
    return text

def check_image_extension(text):
    extensions = ['.jpg','.jpeg', '.tiff', '.raw', '.dng', '.png', '.gif', '.bmp', '.psd']
    for extension in extensions:
        if extension in text:
            return True
    return False
def delete_image_extension(text):
    extensions = ['.jpg','.jpeg', '.tiff', '.raw', '.dng', '.png', '.gif', '.bmp', '.psd']
    for extension in extensions:
        text = text.replace(extension, '')
    return text

def click_to_save_picture(file_name,file_path):
    
    screen_width, screen_height = pyautogui.size()

    # 計算螢幕中心位置
    center_x = screen_width // 2
    center_y = screen_height // 2

    # 將鼠標移動到中心位置
    pyautogui.moveTo(center_x, center_y)
    sleep(1)
    pyautogui.rightClick()
    sleep(1)
    
    # 然後敲擊 V 圖片另存為(v)的快捷鍵是V
    pyautogui.typewrite('v')
    sleep(1)
    
    
    #設置下載路徑,輸完文件名後按6下TAB切到路徑欄
    pyautogui.typewrite(['tab','tab','tab','tab','tab','tab','enter'])
    pyperclip.copy(file_path)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.typewrite(['enter'])
    sleep(0.5)
    
    # alt + s 保存
    pyautogui.hotkey('alt', 's')
    pyautogui.hotkey('alt', 's')
    pyautogui.hotkey('alt', 's')
    pyautogui.hotkey('alt', 's')
    pyautogui.hotkey('alt', 's')
    pyautogui.hotkey('alt', 's')
    pyautogui.hotkey('alt', 's')
    pyautogui.hotkey('alt', 's')

    
    handle = driver.current_window_handle
    handles = driver.window_handles

    # 遍歷窗口

    for newhandle in handles:

        # 關掉多餘窗口

        if newhandle!=handle:

            driver.switch_to.window(newhandle)
            driver.close()
    
    driver.switch_to.window(handle)

def download_file(root_url):
    
    driver.get(root_url)
    
    ### 很難爬的批改結果
    links = driver.find_elements(By.XPATH,"//a[contains(@data-url, '/ajax/sys.pages.course_homework/paperAuditReuslt/')]")
    if len(links) > 0:
        link = links[0]
        data_url = link.get_attribute("data-url")
        
        driver.get('https://eeclass.nthu.edu.tw'+data_url)
            
        pre_element = driver.find_element(By.TAG_NAME, "pre")

        # 获取<pre>标签的内容
        json_data = pre_element.text
        data = json.loads(json_data)
        html_content = data['data']['html']
        
        div_pattern = r'<div class=\'text\'>(.*?)</div>'
        a_pattern = r'<a\b[^>]*>(.*?)</a>'
        matches = re.findall(div_pattern, html_content)
        
        for string in matches:
            # print(match)
            href_pattern = r"href='(.*?)'"
            href_match = re.search(href_pattern, string)

            if not href_match:
                continue
            
            href = href_match.group(1)
            href = href.replace('href:', '').strip()
            # print(href)
            driver.get('https://eeclass.nthu.edu.tw'+href)

            text = string.replace('text:', '').split('(')[0].strip()
            print('正在下載\'' + text + '\'')
            sleep(sleep_time)
        
        wait_for_download()
        sleep(1)

        return 

    ###
    
    
    ### 很好爬的按鈕
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    # 尋找所有的<a>標籤並檢查href屬性是否包含指定的字串
    target_links = []
    all_links = soup.find_all("a")
    dpath = None
    for link in all_links:
        href = link.get("href")
        text = link.text
        
        if href and 'homework/report/' in href:
            dpath = 'https://eeclass.nthu.edu.tw' + href 
            driver.get(dpath)
            break
                    
    if dpath is None:
        return

    li_tags = driver.find_elements(By.XPATH,"//li[contains(@class, 'clearfix')]")
    
    download_path = DOWNLOAD_PATH
    
    # 迭代每個 <li> 標籤
    for li_tag in li_tags:
        
        # 在 <li> 標籤下找到 <a> 標籤
        a_tag = li_tag.find_element(By.TAG_NAME,"a")
        
        # 獲取 <a> 標籤的文字內容和 href 屬性值
        text = a_tag.text
        href = a_tag.get_attribute("href")
        
        # 檢查是否能夠\需要開啟
        if href is None: 
            continue
        
        driver.find_element(By.LINK_TEXT,text).click();
        
        if check_image_extension(text):
            # driver.get(href)
            click_to_save_picture(text,download_path)
        
        print('正在下載\'' + text + '\'')
        sleep(sleep_time)
        
    wait_for_download()
    sleep(1)

def wait_for_download():
    
    download_path = DOWNLOAD_PATH
    
    # Wait for download
    while True:
        files = os.listdir(download_path)
        if len(files) != 0:
            print('Downloading ' + files[0])
        if len(files) >= 0 and not any('.crdownload' in name for name in files) and not any('.tmp' in name for name in files):
            break
        for name in files:
            if name.endswith('.crdownload') or name.endswith('.tmp'):
                continue
            else:
                break
                
            
def course_mkdir(folder_name,target_path):
    
    # 拼接路徑
    folder_path = os.path.join(target_path, folder_name)
    
    if not os.path.exists(folder_path):
        try:
            os.mkdir(folder_path)
            print("[資料夾 \'" + folder_name+ "\' 創建成功]")
        except Exception as e:
            print("[創建資料夾 \'" + folder_name + "\' 時發生錯誤] ", str(e))
    else:
        print("[資料夾 \'" + folder_name + "\' 已存在，跳過創建]")


def move_file(dir_name):
    
    wait_for_download();
    
    download_path = DOWNLOAD_PATH
    destination_path = os.getcwd() + '\\download_file\\' + dir_name

    # 取得原始下載路徑中的所有檔案列表
    files = os.listdir(download_path)
    sleep(0.5)
    
    # iterate所有檔案
    for file in files:
        # 構建原始檔案的完整路徑
        src = os.path.join(download_path, file)
        
        # 構建目標檔案的完整路徑
        dst = os.path.join(destination_path, file)

        # 移動檔案
        shutil.move(src, dst)
        
def download(homeworks):

    course_mkdir(homeworks['course'],os.getcwd()+'\download_file\\')
    
    for homework in homeworks['homework']:
        homework_url = homework['url']
        download_file(homework_url)
        course_mkdir(homework['name'] , os.getcwd()+'\download_file\\'+homeworks['course'])
        move_file(homeworks['course'] +'\\'+homework['name'])
        sleep(sleep_time)
    print('[' + homeworks['course'] + '檔案備份完成]')
    
def get_homework_link(courses):
    
    datas=[]
    for course in courses:
        print('正在爬取\''+course['course']+'\'的作業列表')
        # print(course)
        homework_list_link = "https://eeclass.nthu.edu.tw/course/homeworkList/" + course['token'] 
        driver.get(homework_list_link)
        
        row_datas = driver.find_elements(By.TAG_NAME,"a")
        
        hw_links=[]
        for data in row_datas:
            
            #課程網站連結
            url = data.get_attribute('href') 
            
            #原始作業名稱
            original_title = data.text 
            
            #去除原始作業中的 空白\非法資料夾名稱字元 ... 
            title = format_string(original_title)
            
            if url.find("/course/homework/") != -1:
                hw_links.append({"name" : title , "url" : url})
        
        datas.append({'course' : course['course'] , 'homework' : hw_links})
            
        
    return datas

def get_courses_link():
    
    row_datas = driver.find_elements(By.TAG_NAME,"a")
    datas=[]
    for data in row_datas:
        url = data.get_attribute('href') #課程網站連結
        original_title = data.text #課程名稱
        title = format_string(chinese_string(original_title))
        
        print('正在爬取\''+title+'\'的課程首頁')
        
        if url.find("https://eeclass.nthu.edu.tw/course/") != -1:
            token = url.replace("https://eeclass.nthu.edu.tw/course/","");
            datas.append({"course" : title , "token" : token})  
    
    return datas;

def run():
    
    courses_links = get_courses_link()
        
    # homework_link的架構 example
    # {
    #     'course' : '編譯器設計Compiler Design',
    #     'homework' : 
    #     [
    #         {'name': 'HW1', 'url': 'https://eeclass.nthu.edu.tw/course/homework/22xxx'},
    #         {'name': 'HW2', 'url': 'https://eeclass.nthu.edu.tw/course/homework/24xxx'},
    #         {'name': 'HW3', 'url': 'https://eeclass.nthu.edu.tw/course/homework/25xxx'}
    #     ]
    # }
        
    homework_links = get_homework_link(courses_links) 
    for homework in homework_links:
        download(homework)

def delete_empty_directory():
    
    print('[開始刪除空白資料夾]')

    path = os.getcwd() + '\\' + 'download_file' + '\\'
    dirs = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    for dir in dirs:
        
        sub_path = path + '\\' + dir
        sub_dirs = [name for name in os.listdir(sub_path) if os.path.isdir(os.path.join(sub_path, name))]
        
        for sub_dir in sub_dirs:
            sub_sub_path = sub_path + '\\' + sub_dir
            number_of_subsubcontents = len(os.listdir(sub_sub_path)) 
            # print(dir + ' ' + str(number_of_subsubcontents))
            # 檢查資料夾是否為空
            if number_of_subsubcontents == 0:
                # 刪除資料夾
                os.rmdir(sub_sub_path)
        
        
        
        number_of_subcontents = len(os.listdir(path+dir)) 
        # 檢查資料夾是否為空
        if number_of_subcontents == 0:
            # 刪除資料夾
            os.rmdir(sub_path)
    
    print('[結束刪除空白資料夾]')
            
def main():
    
    run()
    delete_empty_directory();
    driver.quit();
        
if __name__ == "__main__":
    
    print("----------PROGRAM START--------")
    main()
    print("----------PROGRAM END----------")
    