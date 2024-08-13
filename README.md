# Kubernetes Event Driven Autoscaler


### Install KEDA to the cluster:
```
kubectl apply --server-side -f https://github.com/kedacore/keda/releases/download/v2.14.1/keda-2.14.1.yaml
```

#### Uninstall KEDA
```
kubectl delete -f https://github.com/kedacore/keda/releases/download/v2.14.1/keda-2.14.1.yaml
```


### Setup RabbitMQ to the cluster in internal namespace
```
cd helm-rabbitmq
./install.sh
```
*Note: You can update rabbitmq default username and password in values.yaml auth section*

#### Uninstall RabbitMQ
```
helm delete rabbitmq -n internal
```


### Deploy application to the cluster
```
helm upgrade -i <chart name> ./deploy -n <namespace>
```

#### Uninstall app
```
helm delete <chart name> -n <namespace>
```


### Publish Message to RabbitMQ
```
cd rabbitmq-publisher
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
*Note: You need to port-forward rabbitmq service in order to connect to rabbitmq locally. Also, update the rabbitmq credentials if required.*