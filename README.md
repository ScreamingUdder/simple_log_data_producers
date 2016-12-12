# simple_log_data_producers
Very simple Kafka log producers, intended to be used for experimenting with Kafka-Connect and ELK

## Setting up Kafka and Elastic Stack

Download and extract Confluent package v3.0.1 (includes Kafka, Kafka-Connect, Schema Repository) from https://www.confluent.io/download/.
N.B. Confluent 3.0.1 claims to include the Elasticsearch connector, but I could not get it to work or find any evidence that it is actually there, so I downloaded and built the connector separately.

Download and extract Kafka-Connect-Elasticsearch:
```
wget https://github.com/confluentinc/kafka-connect-elasticsearch/archive/v3.1.0-rc1.tar.gz
tar -xzf v3.1.0-rc1.tar.gz
 ```
In the extracted connect module files edit `pom.xml` so that the Kafka version line reads:
```
<kafka.version>0.10.0.1</kafka.version>
```
then install Maven and build the module:
```
apt-get install maven
cd kafka-connect-elasticsearch-3.1.0-rc1
mvn clean package -DskipTests
```
From the Confluent directory start Zookeeper, Kafka and the Schema registry (in separate terminals):
```
./bin/zookeeper-server-start ./etc/kafka/zookeeper.properties

./bin/kafka-server-start ./etc/kafka/server.properties

./bin/schema-registry-start ./etc/schema-registry/schema-registry.properties
```
Edit `confluent-3.0.1/etc/kafka/connect-standalone.properties` so that the key and value converter properties are:
```
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=io.confluent.connect.avro.AvroConverter
value.converter.schema.registry.url=http://localhost:8081

key.converter.schemas.enable=false
value.converter.schemas.enable=true
```
Create a file called `elasticsearch-kafka-connect.properties` in the confluent package directory, with these contents:
```
name=elasticsearch-sink
connector.class=io.confluent.connect.elasticsearch.ElasticsearchSinkConnector
tasks.max=1
connection.url=http://localhost:9200
type.name=kafka-connect
# Custom config
topics=log_data_test12
topic.schema.ignore=log_data_test12
key.ignore=true
```

Find the path to the `kafka-connect-elasticsearch-3.1.0.jar` which you built, it should be in `kafka-connect-elasticsearch-3.1.0-rc1/target`. Then start the Kafka-Connect module:
```
export CLASSPATH=/path/to/elasticsearch/connector/*

./bin/connect-standalone etc/kafka/connect-standalone.properties elasticsearch-kafka-connect.properties
```
I created some very simple producers with Python. Scripts are here: https://github.com/ScreamingUdder/simple_log_data_producers. The Kibana interface is at localhost:5601. This article guides through the last step of configuring Kibana: https://www.confluent.io/blog/streaming-data-oracle-using-oracle-goldengate-kafka-connect/

Setting up a dynamic mapping for a time field is a critical step in configuring Kafka. This tells Kibana how to recognise when a string field represents a timestamp. The dynamic mapping can be set via Kibana's REST interface using Curl. This example looks for a field called "datetime" and tells Kibana to parse the string and record it as a "date" type. This field can then be selected as the time field in the Kibana interface.

```
curl -XPUT 'localhost:9200/demo_9?pretty' -d'
{
  "mappings": {
    "kafka-connect": {
      "dynamic_templates": [
        {
          "dates": {
            "match": "datetime",
  "mapping": {
              "type": "date",
 "format": "YYYY-MM-dd HH:mm:ss"
            }
          }
        }
      ]
    }
  }
}'
```


