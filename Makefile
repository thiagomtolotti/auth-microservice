.PHONY: dev generate-certs tests tests-watch 

args =

dev:
	sudo docker compose up --build dev --remove-orphans

generate-certs:
	mkdir -p certs
	openssl genrsa -out certs/private_key.pem 2048
	openssl rsa -in certs/private_key.pem -pubout -out certs/public_key.pem
	chmod 600 certs/private_key.pem

tests: 
	sudo docker-compose run --build --rm tests $(args)

tests-watch:
	sudo docker-compose run --build --rm tests-watch

coverage:
	sudo docker-compose run --build --rm coverage