# exec(open('src/data_fetch/__main__.py', encoding='utf-8').read())

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re
import os
from timeit import default_timer as timer

def print_time(message, start_time):
  now = timer()
  print(message, now - start_time, '秒')
  return now

def main():
  now = print_time('開始', timer())

  options = Options()
  options.add_argument('--disable-notifications')
  options.add_experimental_option("detach", True)
 # options.add_argument('--headless')

  chrome = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)
  chrome.get('https://academics.ntou.edu.tw/?lnk=32')

  now = print_time('網站開啟完成', now)

  # 顯示體育課資料
  chrome.switch_to.frame('mainFrame')

  while True:
    faculty_select = Select(chrome.find_element(By.ID, 'Q_FACULTY_CODE'))
    faculty_select.select_by_value('0902') # 體育室

    pagesize_input = chrome.find_element(By.ID, 'PC_PageSize')
    pagesize_input.send_keys(Keys.CONTROL + 'a')
    pagesize_input.send_keys(Keys.DELETE)
    pagesize_input.send_keys('1000')

    chrome.find_element(By.ID, 'QUERY_BTN1').click()

    now = print_time('按下按鈕', now)

    # 取得表格
    data_table = WebDriverWait(chrome, 10).until(
      EC.presence_of_element_located((By.ID, 'DataGrid'))
    )
    df = pd.read_html(data_table.get_attribute('outerHTML'))[0]

    now = print_time('取得表格', now)

    # 取出人數上限
    max_people = []
    for val in df['人數限制上／下限']:
      max_people.append(int(re.search(r'^\d*', val).group()))
    df['人數上限'] = max_people

    # 刪除人數為0的課程
    df = df[df['人數'] != 0]

    # 計算剩餘人數並排序
    df['剩餘人數'] = df['人數上限'] - df['人數']
    df = df.sort_values(by=['剩餘人數'], ascending=False)

    now = print_time('表格處理結束', now)

    # 輸出
    os.makedirs('data', exist_ok=True)
    # df.to_csv('data/ntou_academy_sports.csv', index=False, encoding='big5')
    with open('data/ntou_academy_sports.md', 'w', encoding='utf-8') as f:
      f.write(df.to_markdown())
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #   print(df)

    now = print_time('結束', now)
    time.sleep(10)
    now = print_time('重新開始', now)

if __name__ == '__main__':
  main()