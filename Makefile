.PHONY: dev generate-certs tests tests-watch venv

args =

dev:
	docker compose up --build dev --remove-orphans

generate-certs:
	mkdir -p certs
	openssl genrsa -out certs/private_key.pem 2048
	openssl rsa -in certs/private_key.pem -pubout -out certs/public_key.pem
	chmod 600 certs/private_key.pem

tests: 
	docker-compose run --build --rm tests ${path}

tests-watch:
	docker-compose run --build --rm tests-watch pytest-watch ${path}

coverage:
	docker-compose run --build --rm coverage

venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt