run-dev:
	poetry run streamlit run src/frontend.py

build:
	docker build -t transaction-generator .

run: build
	docker run \
		--network=redpanda_network \
		-p 8501:8501 \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		--env N_TRANSACTIONS_PER_SECOND=10 \
		transaction-generator