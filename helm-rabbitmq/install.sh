#!/bin/bash

kubectl create namespace internal
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade -i -f values.yaml rabbitmq bitnami/rabbitmq -n internal