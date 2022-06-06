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

class CourseDataFetcher:
  def __init__(self):
    self.options = Options()
    self.options.add_argument('--disable-notifications')
    self.options.add_experimental_option("detach", True)

    # self.options.add_argument('--headless')

    self.course_data_url = 'https://academics.ntou.edu.tw/?lnk=32'

  def __enter__(self):
    self.driver = webdriver.Chrome(
      service = Service(ChromeDriverManager().install()),
      options=self.options,
      service_log_path='NUL' # windows
    )
    self.driver.get(self.course_data_url)
    self.driver.switch_to.frame('mainFrame')

  def __exit__(self, exc_type, exc_value, traceback):
    self.driver.quit()

  def fetch_course_data(self, faculty_code, grade=''):
    faculty_select = Select(self.driver.find_element(By.ID, 'Q_FACULTY_CODE'))
    faculty_select.select_by_value(faculty_code)
    grade_select = Select(self.driver.find_element(By.ID, 'Q_GRADE'))
    grade_select.select_by_value(grade)
    pagesize_input = self.driver.find_element(By.ID, 'PC_PageSize')
    pagesize_input.send_keys(Keys.CONTROL + 'a')
    pagesize_input.send_keys(Keys.DELETE)
    pagesize_input.send_keys('1000')

    self.driver.find_element(By.ID, 'QUERY_BTN1').click()
    loading_icon = WebDriverWait(self.driver, 30).until(
      EC.invisibility_of_element_located((By.ID, '__LOADINGBAR'))
    )
    data_table = WebDriverWait(self.driver, 30).until(
      EC.presence_of_element_located((By.ID, 'DataGrid'))
    )
    course_df = pd.read_html(data_table.get_attribute('outerHTML'))[0]
    course_df = self.__clean_course_df(course_df)

    return course_df
  
  def __clean_course_df(self, origin_df):
    df = origin_df.copy()

    # get limit of selected people
    max_people = []
    for val in df['人數限制上／下限']:
      max_people.append(int(re.search(r'^\d*', val).group()))
    df['人數上限'] = max_people

    # delete rows with no people selected
    df = df[df['人數'] != 0]

    # calculate selected people left
    df['剩餘人數'] = df['人數上限'] - df['人數']

    # sort by selected people left
    df = df.sort_values(by=['剩餘人數'], ascending=False)

    return df

if __name__ == '__main__':
  course_fetcher = CourseDataFetcher()
  with course_fetcher:
    course_df = course_fetcher.fetch_course_data('0902')
    print(course_df)
    os.makedirs('data', exist_ok=True)
    # df.to_csv('data/ntou_academy_sports.csv', index=False, encoding='big5')
    # with open('data/ntou_academy_sports.md', 'w', encoding='utf-8') as f:
    #   f.write(df.to_markdown())
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #   print(df)