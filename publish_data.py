from confluent_kafka import Producer
import time
import device
import json


def create_message(log_device):
    # create json message
    # name and value

    return 'blargh'


def main():
    # Create producer
    p = Producer({'bootstrap.servers': 'sakura,hinata,tenten'})

    # Create devices
    devices = [device.SampleTemperature()]

    # Time step loop
    timestep = 1  # seconds
    current_time = 0
    while True:
        time.sleep(timestep)
        current_time += timestep
        for dev in devices:
            p.produce('log_data_test', create_message(dev).encode('utf-8'))
        p.flush()


if __name__ == "__main__":
    main()
