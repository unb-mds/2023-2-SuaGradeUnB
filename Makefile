all: copy-env setup-env config-mock entrypoint-chmod
copy-env: 
	cp ./api/.env.example ./api/.env

setup-env: 
	bash scripts/env.sh

config-mock:
	bash scripts/config.sh

entrypoint-chmod:
	chmod +x ./api/entrypoint.sh
