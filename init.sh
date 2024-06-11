#!/usr/bin/env bash

until printf "" 2>>/dev/null >>/dev/tcp/127.0.0.1/9042; do 
    sleep 5;
    echo "Waiting for cassandra...";
done

echo "Creating keyspace and tables..."
cqlsh 127.0.0.1 -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS flights_system WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};"