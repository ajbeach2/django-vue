test:
	docker-compose up -d && \
	docker-compose exec api make test && \
	docker-compose exec client npm run test:unit

stop:
	docker-compose down -v

clean: stop
	yes | docker system prune

start:
	docker-compose up

dbstart:
	docker-compose up -d postgres

dbstop:
	docker-compose stop postgres