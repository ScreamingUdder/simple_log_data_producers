from confluent_kafka import Producer
import time
import device
import json


def create_message(log_device):
    """Create json message"""
    msg = {'name': log_device.get_name(),
           'value': log_device.get_value()}
    return json.dumps(msg)


def main():
    # Create producer
    conf = {'bootstrap.servers': 'sakura,hinata,tenten'}
    p = Producer(**conf)

    # Create devices
    devices = [device.SampleTemperature(), device.Oscillator()]

    # Time step loop
    timestep = 1  # seconds
    current_time = 0
    while True:
        time.sleep(timestep)
        current_time += timestep
        print current_time
        for dev in devices:
            p.produce('log_data_test', create_message(dev).encode('utf-8'))
        p.flush()


if __name__ == "__main__":
    main()
