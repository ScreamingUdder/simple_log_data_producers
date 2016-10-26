from confluent_kafka import Producer
import time
import device
import requests
import avro.schema
import avro.io
import io
import json


def create_avro_message(log_device, writer):
    """Create message bytes using Avro schema"""
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)

    writer.write({"name": log_device.get_name(), "value": log_device.get_value()}, encoder)

    return bytes_writer.getvalue()


def create_json_message(log_device):
    """Create json message"""
    msg = {'name': log_device.get_name(),
           'value': log_device.get_value()}
    return json.dumps(msg)


def main():
    # Create Avro schema
    test_schema = '''
    {
    "namespace": "example.avro",
     "type": "record",
     "name": "SampleLog",
     "fields": [
         {"name": "name", "type": "string"},
         {"name": "value",  "type": "float"}
     ]
    }
    '''
    schema = avro.schema.parse(test_schema)
    writer = avro.io.DatumWriter(schema)

    # Create producer
    conf = {'bootstrap.servers': 'localhost'}
    p = Producer(**conf)

    print 'Schema:'
    schema_string = json.dumps(schema.to_json()).encode('utf-8')
    schema_string = "".join(schema_string.split())
    print schema_string

    # Register schema
    schema_reg_url = 'http://localhost:8081'
    r = requests.post(schema_reg_url + '/subjects/log_data_test2-value/versions',
                      data={'schema': schema_string},
                      headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'})

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
            p.produce('log_data_test2', create_avro_message(dev, writer))
            p.produce('log_data_test3', create_json_message(dev))
        p.flush()


if __name__ == "__main__":
    main()
