FROM    docker.elastic.co/elasticsearch/elasticsearch:8.13.1

# Copy configuration files
COPY    healthcheck.sh          ./
COPY    elasticsearch.yml       config/
COPY    jvm.options             config/jvm.options.d/

# Define exposed ports
EXPOSE  9200
