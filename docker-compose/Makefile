## Commands to start and stop the ML inference pipeline

start-ml-inference-pipeline:
	docker compose -f ml_inference_pipeline.yml up -d

stop-ml-inference-pipeline:
	docker compose -f ml_inference_pipeline.yml down


## Commands to start and stop the infrastructure

# Redpanda for the communication between the services
start-redpanda:
	docker compose -f redpanda.yml up -d

stop-redpanda:
	docker compose -f redpanda.yml down

# Prometheus and Grafana for monitoring
start-prometheus-and-grafana:
	docker compose -f prometheus_and_grafana.yml up -d

stop-prometheus-and-grafana:
	docker compose -f prometheus_and_grafana.yml down