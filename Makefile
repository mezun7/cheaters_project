.PHONY: PHONY
PHONY:

init: PHONY
	docker-compose up --build collectstatic init_db

start: PHONY
	docker-compose up nginx go_app

stop: PHONY
	docker-compose down

# stop everything
stop_all: PHONY
	docker stop $(docker ps -a -q)

# show all containers
list: PHONY
	docker ps -a