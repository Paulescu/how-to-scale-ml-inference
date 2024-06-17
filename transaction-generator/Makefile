run-dev:
	poetry run python -m src.main --n_transactions_per_second 100

build:
	docker build -t transaction-generator .

run: build
	docker run \
		--network=redpanda_network \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		transaction-generator