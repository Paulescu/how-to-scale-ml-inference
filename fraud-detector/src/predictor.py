from typing import List, Dict

class MyModel:
    """
    A Mocked ML model that randomly predicts if a transaction is fraudulent or not
    with a probability of 0.05 for fraud and 0.95 for non-fraud.
    """
    def __init__(self, latency_ms: int):
        self.latency_ms = latency_ms

    def predict(self, X: Dict) -> float:
        """
        Randomly predicts if the given transaction `X` is fraudulent or not
        with a probability of 0.05 for fraud and 0.95 for non-fraud.

        Args:
            X: A dictionary containing the transaction details

        Returns:
            0 if the transaction is non-fraudulent
            1 if the transaction is fraudulent
        """
        # returns either 0 with probability 0.95 or 1 with probability 0.05
        import random
        from time import sleep
        
        # sleep for `self.latency_ms` to simulate the time taken to make a prediction
        sleep(self.latency_ms / 1000.0)

        return 0 if random.random() < 0.95 else 1.0