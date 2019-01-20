# EasyEye 
## Time and location
- HackCambridge 4D on 19 Jan 2019
## Member
- Li Rui: Frontend Design
- Lin Weizhe: Data Structure Design, Backend Design
- Zheng Hehui: Backend Data Analyser
- Wu Xiaodong: Facial Detection

## Intro
This is the git repo for the 2019 Hack Cambridge
## Source
### database_backup
file of dumped database of hackathon
### src/website
Django server for hackathon
### src/Fitbit
Fitbit codes of watch frontend
### src/facial detection
Facial landmark detection and data uploading

## Run the code
### Django server
```angular2html
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
### Evaluator
```angular2html
export DJANGO_SETTINGS_MODULE=EasyEye.settings
python evaluation_tool.py
```
### Facial Detection
#### 1st step: Download dlib/OpenCV and install

#### 2st step: Run the code
```angular2html
python feature_extraction.py
```