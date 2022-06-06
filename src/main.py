from course_data_fetcher.course_data_fetcher import CourseDataFetcher
import pandas as pd
import os
import time
import logging

os.makedirs('logs', exist_ok=True)
logging.basicConfig(
  filename='logs/course_data_fetcher.log',
  level=logging.INFO,
  format='[%(levelname)s] %(message)s (%(asctime)s)',
  encoding='utf-8'
)

course_fetcher = CourseDataFetcher()
with course_fetcher:
  last_course_df = course_fetcher.fetch_course_data('0902')
  last_course_df = pd.concat([last_course_df, course_fetcher.fetch_course_data('0507')])
  last_course_df = pd.concat([last_course_df, course_fetcher.fetch_course_data('090M')])
  last_course_df = last_course_df.set_index(['課號', '年級班別'])
  # last_course_df.loc[('B92A6G04', '1年A班'), '剩餘人數'] = 100 # for testing
  search_times = 0
  while True:
    time.sleep(10)
    print(f'Searching... {search_times}')
    search_times += 1
    course_df = course_fetcher.fetch_course_data('0902')
    course_df = pd.concat([course_df, course_fetcher.fetch_course_data('0507')])
    course_df = pd.concat([course_df, course_fetcher.fetch_course_data('090M')])
    course_df = course_df.set_index(['課號', '年級班別'])
    for index, row in course_df.iterrows():
      if index in last_course_df.index:
        if row['剩餘人數'] > last_course_df.loc[index, '剩餘人數']:
          logging.info(f'-有人退選了 {row["課名"]}{index}, 剩餘空位: {row["剩餘人數"]}人')
        elif row['剩餘人數'] < last_course_df.loc[index, '剩餘人數']:
          logging.info(f'+有人加選了 {row["課名"]}{index}, 剩餘空位: {row["剩餘人數"]}人')
    last_course_df = course_df

    os.makedirs('data', exist_ok=True)
    with open('data/ntou_academy_sports.md', 'w', encoding='utf-8') as f:
      f.write(course_df.to_markdown())
