run-dev:
	poetry run python -m src.main

build:
	docker build -t fraud-detector .

run: build
	docker run \
		--network=redpanda_network \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		--env ML_MODEL_LATENCY_MS=100 \
		fraud-detector