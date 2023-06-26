SHELL:=/bin/bash

install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt &&\
	pip install -r ./label-reader/modules/label_extraction/requirements.txt &&\
	pip install -r ./label-reader/modules/web_app_api/requirements.txt

web_app_api_tests:
	coverage run --source=./label-reader/modules/web_app_api -m nose2 --plugin nose2.plugins.junitxml --junit-xml --junit-xml-path ./label-reader/modules/web_app_api/nose2-junit.xml --verbose -s ./label-reader/modules/web_app_api tests && coverage html -d ./label-reader/modules/web_app_api/htmlcov && coverage xml -o ./label-reader/modules/web_app_api/coverage.xml

label_extraction_tests:
	coverage run --source=./label-reader/modules/label_extraction -m nose2 --plugin nose2.plugins.junitxml --junit-xml --junit-xml-path ./label-reader/modules/label_extraction/nose2-junit.xml --verbose -s ./label-reader/modules/label_extraction tests && coverage html -d ./label-reader/modules/label_extraction/htmlcov && coverage xml -o ./label-reader/modules/label_extraction/coverage.xml

all: install tests

start-label-extraction:
	set -o allexport && source .env && python label-reader/modules/label_extraction/main.py

start-web-app-api:
	set -o allexport && source .env && python label-reader/modules/web_app_api/main.py

start-web-app:
	set -o allexport && source .env && docker run --name web_app -v $(shell pwd)/label-reader/modules/web_app_ui_mvp:/usr/share/nginx/html:ro -it --rm -p 8081:80 nginx

start-all:
	set -o allexport && source .env && python label-reader/modules/label_extraction/main.py &
	set -o allexport && source .env && python label-reader/modules/web_app_api/main.py &
	set -o allexport && source .env && docker run --name web_app -v $(shell pwd)/label-reader/modules/web_app_ui_mvp:/usr/share/nginx/html:ro -d --rm -p 8081:80 nginx

start-rtsp-server:
	set -o allexport && source .env && docker run -d --rm --name=rtsp-simple -e RTSP_PROTOCOLS=tcp -p 8554:8554  aler9/rtsp-simple-server