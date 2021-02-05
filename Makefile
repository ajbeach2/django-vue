test:
	docker-compose exec api make test && \
	docker-compose exec client npm run test:unit