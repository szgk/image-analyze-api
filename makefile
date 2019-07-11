VER=75

build:
	sh shell/build.sh && make driver VER=74

dev:
	sh shell/up.sh DEV=1

update:
	pip freeze > requirements.txt

clear:
	find . -name "__pycache__" -exec rm -rf {} \;
	find ../public/img/ -name "*.png" -exec rm -rf {} \;

driver:
	cp ./drivers/chromedriver_${VER} ./drivers/chromedriver

test_unit:
	python test/modules/TestColors.py
