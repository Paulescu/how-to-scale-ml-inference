from threading import Thread

import streamlit as st

# from src.config import config
from src.produce_transaction import (
    produce_transactions,
    shared_data
)

# Start a background thread to produce transactions to the
# Kafka topic
thread = Thread(target=produce_transactions)
thread.daemon = True
thread.start()

def run_app():

    st.sidebar.title("Transaction Generator")

    # a stremlit component to get the number of transactions per second
    n_transactions_per_second = st.number_input(
        label="Number of transactions per second",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
    )

    # with shared_data_lock:
    shared_data['n_transactions_per_second'] = n_transactions_per_second
    
    st.write(f"Producing {n_transactions_per_second} transactions per second")
    
if __name__ == '__main__':

    run_app()


