# NTOUCourseInquirer

## HOW TO USE

這裡都以windows為主

### prerequire

安裝python3

### setup

從終端機(如cmd)切換到這個資料夾

並開個虛擬環境下載相關套件
```bash
python -m pip install virtualenv
python -m venv venv
.\venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### run

```bash
.\venv\Scripts\activate.bat
python src/main.py
```

擺著，純文字紀錄會慢慢出現在logs資料夾

建議用個vscode之類會自動更新文字的編輯器看

而所有人數結果會在data資料夾，markdown格式

但有點亂亂的:D

## note

目前還爛爛的，有時候跑一跑網路不好或網站卡會跳掉

預設查通識、體育、資工的所有課

懶得做使用者輸入了，要改的話去`src/main.py`通靈一下

祝各位搶的到想要的課，下次更新應該是下學期了

有問題歡迎問