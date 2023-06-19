gimie API Helm chart

To install the chart, you will need to provide your github and gitlab tokens as values to generate secrets. This can be done as follows:

1. Prepare a `secrets.yaml` file with your tokens:

```
# secrets.yaml
github: <your-github-token>
gitlab: <your-gitlab-token>
```

2. Install the chart, provding your secrets as values.

```sh
helm install -f secrets.yaml gimie ./gimie-api
```

If you are using minikube, you can then get the endpoint using:

```sh
minikube service --all
```
