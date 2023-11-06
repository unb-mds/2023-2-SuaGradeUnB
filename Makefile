## Base Makefile ##

# Configuration
config: copy-env setup-env config-mock entrypoint-chmod
copy-env: 
	cp ./api/.env.example ./api/.env

setup-env: 
	bash scripts/env.sh

config-mock:
	bash scripts/config.sh

entrypoint-chmod:
	chmod +x ./api/entrypoint.sh

# Install Dependencies
install:
	pip install -r requirements.txt
	npm install --prefix ./web


## Docker ##

start:
	sudo docker compose up -d 

start-b:
	sudo docker compose up --build -d

stop:
	sudo docker compose down

stop-v:
	sudo docker compose down -v 


## Django Shortcuts ##

# Tests
test:
	python3 scripts/test.py --clean

testfull: 
	python3 scripts/test.py
	sudo docker exec django-api coverage html
	python3 scripts/report.py

cleanup:
	sudo rm -f api/.coverage
	sudo rm -f -r api/htmlcov

# Migrations
makemigrations:
	sudo docker exec django-api python3 manage.py makemigrations

migrate:
	sudo docker exec django-api python3 manage.py migrate
