.PHONY: build

build:
	@docker-compose \
					-f docker-compose.yaml \
					build --no-cache

build-qaw:
	@docker-compose \
					-f docker-compose.qaw.yaml \
					build --no-cache

build-prod:
	@docker-compose \
					-f docker-compose.prod.yaml \
					build

deploy:
	@docker-compose \
					-f docker-compose.yaml \
					up --build --remove-orphans -d

deploy-qaw:
	@docker-compose \
					-f docker-compose.qaw.yaml \
					up --build --remove-orphans -d

deploy-prod:
	@docker-compose \
					-f docker-compose.prod.yaml \
					--env-file build/env/.env.prod \
					up --build --force-recreate -d

down:
	@docker-compose \
					-f docker-compose.yaml \
					down --remove-orphans -v

down-qaw:
	@docker-compose \
					-f docker-compose.qaw.yaml \
					down --remove-orphans -v

down-prod:
	@docker-compose \
					-f docker-compose.prod.yaml \
					down --rmi all --remove-orphans -v

refresh-db:
	@sh build/bin/refresh-db.sh

