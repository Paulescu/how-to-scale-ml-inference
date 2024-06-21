run-dev:
	poetry run python -m src.main

build:
	docker build -t latency-monitor .

run: build
	docker run \
		--network=redpanda_network \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		latency-monitor