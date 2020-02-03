include .env
export

DOCKER_COMPOSE=docker-compose -f docker-compose.yml

# make sure we don't run into problems if there is a file with the same name as one of these commands
.PHONY: pip-install \
    stop \
    destroy \
    purge-images \
    purge-vendor \
    purge-all \
    build \
    rebuild-images \
    rebuild-all \
    run \
    logs \
    shell

default: run

stop:
	${DOCKER_COMPOSE} down

destroy:
	${DOCKER_COMPOSE} down -v --remove-orphans

purge-images:
	-docker rmi -f `docker image ls | grep "${PROJECT_SLUG}" | awk '{print $$3}' | uniq`

purge-vendor:
	rm -rf ./vendor/*
	rm -rf ./static/*

purge-all: destroy purge-images purge-vendor

build:
	SKIP_BUILD=0 ${DOCKER_COMPOSE} run builder

shell:
	docker exec -ti --env COLUMNS=`tput cols` --env LINES=`tput lines` `docker ps| grep "${PROJECT_SLUG}_backend" | awk '{print $$1}'` bash

rebuild-images: purge-images build

rebuild-all: purge-all build

run:
	SKIP_RUN=0 ${DOCKER_COMPOSE} up -d

logs:
	${DOCKER_COMPOSE} logs -tf