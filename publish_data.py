from confluent_kafka import Producer
import time
import device
import requests
import avro.schema
import avro.io
import io
import json


def create_avro_message(log_device, writer, id):
    """Create message bytes using Avro schema"""
    # Initialise with magic byte = 0 and 4 byte schema id
    # TODO use id rather than hardcoding id
    kafka_magic = io.BytesIO(b'\x00\x00\x00\x00\x15')
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)

    writer.write({"name": log_device.get_name(), "value": log_device.get_value(), "time": log_device.get_time()}, encoder)

    return kafka_magic.getvalue() + bytes_writer.getvalue()


def main():
    # Create Avro schema
    test_schema = '''
    {
    "namespace": "example.avro",
     "type": "record",
     "name": "SampleLog",
     "fields": [
         {"name": "name", "type": "string"},
         {"name": "value",  "type": "float"},
         {"name": "time", "type": "float"}
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

    # Topic
    topic_name = 'demo_2'

    # Register schema
    schema_reg_url = 'http://localhost:8081'
    r = requests.post(schema_reg_url + '/subjects/' + topic_name + '-value/versions',
                      data=json.dumps({'schema': schema_string}).encode('utf-8'),
                      headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'})
    schema_id = json.loads(r.text)["id"]
    print 'Schema id: ' + str(json.loads(r.text)["id"])

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
            p.produce(topic_name,
                      value=create_avro_message(dev, writer, schema_id))
            dev.update(timestep)
        p.flush()


if __name__ == "__main__":
    main()
