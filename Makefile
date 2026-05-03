.PHONY: dev generate-certs tests

dev:
	sudo docker-compose run --build --rm dev

generate-certs:
	mkdir -p certs
	openssl genrsa -out certs/private_key.pem 2048
	openssl rsa -in certs/private_key.pem -pubout -out certs/public_key.pem
	chmod 600 certs/private_key.pem

tests: 
	sudo docker-compose run --build --rm tests