.PHONY: dev

dev:
	sudo docker compose run --rm --remove-orphans web python app/main.py