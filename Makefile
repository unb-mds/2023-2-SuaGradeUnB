all: copy-env setup-env config-mock
copy-env: 
	cp ./api/.env.example ./api/.env

setup-env: 
	bash scripts/env.sh

config-mock:
	bash scripts/config.sh
