import time
import json
from confluent_kafka import Producer
import numpy as np
from statsmodels.tsa.arima_process import arma_generate_sample

# Kafka configuration
conf = {'bootstrap.servers': 'kafka:9092'}

# Create Producer instance
p = Producer(**conf)

# ARMA parameters
ar_params = np.array([.75, -.25])
ma_params = np.array([.65, .35])
n_sample = 1
sigma = 0.01

# Generate ARMA(2, 2) sample
arma_series = arma_generate_sample(np.r_[1, -ar_params], np.r_[1, ma_params], n_sample, sigma)

# Kafka topic
topic = 'raw-data'

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()}")

# Continuously generate ARMA(2, 2) samples and send to Kafka topic
while True:
    arma_series = arma_generate_sample(np.r_[1, -ar_params], np.r_[1, ma_params], n_sample, sigma)
    data = {'value': float(arma_series[0])}
    p.produce(topic, json.dumps(data), callback=delivery_report)
    p.flush()
    time.sleep(2)
