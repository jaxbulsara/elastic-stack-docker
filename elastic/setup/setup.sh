#!/bin/bash

if [ x${ES_PASSWORD} == x ]; then
  echo "Set the ES_PASSWORD environment variable in the .env file"
  exit 1
elif [ x${KB_PASSWORD} == x ]; then
  echo "Set the KB_PASSWORD environment variable in the .env file"
  exit 1
fi

if [ ! -f config/certs/ca.zip ]; then
  echo "Creating Certificate Authority"

  bin/elasticsearch-certutil ca \
    --silent \
    --pem \
    -out config/certs/ca.zip

  unzip config/certs/ca.zip -d config/certs
fi

if [ ! -f config/certs/certs.zip ]; then
  echo "Creating certs"

  bin/elasticsearch-certutil cert \
    --silent \
    --pem \
    -out config/certs/certs.zip \
    --in instances.yml \
    --ca-cert config/certs/ca/ca.crt \
    --ca-key config/certs/ca/ca.key

  unzip config/certs/certs.zip -d config/certs
fi

echo "Setting file permissions"

chown -R root:root config/certs
find config/certs -type d -exec chmod 755 \{\} \;
find config/certs -type f -exec chmod 644 \{\} \;

echo "Waiting for Elasticsearch availability"
until
  curl -s --cacert config/certs/ca/ca.crt https://elasticsearch:9200 |
    grep -q "missing authentication credentials"
do
  sleep 30
done

echo "Setting kibana_system password"
until
  curl -s -X POST \
    --cacert config/certs/ca/ca.crt \
    -u "elastic:${ES_PASSWORD}" \
    -H "Content-Type: application/json" \
    https://elasticsearch:9200/_security/user/kibana_system/_password \
    -d "
      {
        \"password\": \"${KB_PASSWORD}\"
      }
      " |
    grep -q '^{}'
do
  sleep 10
done

echo "Creating logstash_writer role"
until
  curl -s -X POST \
    --cacert config/certs/ca/ca.crt \
    -u "elastic:${ES_PASSWORD}" \
    -H "Content-Type: application/json" \
    https://elasticsearch:9200/_security/role/logstash_writer \
    -d '
      {
        "cluster": ["manage_index_templates", "monitor", "manage_ilm"],
        "indices": [
          {
            "names": [ "logstash-*", "logs-generic-default" ],
            "privileges": ["write","create","create_index","manage","manage_ilm"]
          }
        ]
      }
      ' |
    grep -q '^{"role":{"created":true}}'
do
  sleep 10
done

echo "Creating logstash_internal user"
until
  curl -s -X POST \
    --cacert config/certs/ca/ca.crt \
    -u "elastic:${ES_PASSWORD}" \
    -H "Content-Type: application/json" \
    https://elasticsearch:9200/_security/user/logstash_internal \
    -d "
      {
        \"password\" : \"${LS_PASSWORD}\",
        \"roles\" : [ \"logstash_writer\"],
        \"full_name\" : \"Internal Logstash User\"
      }
      " |
    grep -q '^{"created":true}'
do
  sleep 10
done

echo "Creating logstash_reader role"
until
  curl -s -X POST \
    --cacert config/certs/ca/ca.crt \
    -u "elastic:${ES_PASSWORD}" \
    -H "Content-Type: application/json" \
    https://elasticsearch:9200/_security/role/logstash_reader \
    -d '
      {
        "cluster": ["manage_logstash_pipelines"]
      }
      ' |
    grep -q '^{"role":{"created":true}}'
do
  sleep 10
done

echo "Creating logstash_user user"
until
  curl -s -X POST \
    --cacert config/certs/ca/ca.crt \
    -u "elastic:${ES_PASSWORD}" \
    -H "Content-Type: application/json" \
    https://elasticsearch:9200/_security/user/logstash_user \
    -d "
      {
        \"password\" : \"${KB_PASSWORD}\",
        \"roles\" : [ \"logstash_reader\", \"logstash_admin\"],
        \"full_name\" : \"Kibana User for Logstash\"
      }
      " |
    grep -q '^{"created":true}'
do
  sleep 10
done

echo "Completed."
