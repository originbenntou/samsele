```
# path/to/.aws/credentials
[localstack]
aws_access_key_id = dummy
aws_secret_access_key = dummy

# path/to/.aws/config
[profile localstack]
region = ap-northeast-1
output = json
```

```
docker-compose up -d
```

```
 aws s3api list-buckets --endpoint-url=http://localhost:4566 --profile s3local
```

```
sam build --use-container --build-image amazon/aws-sam-cli-build-image-python3.6
```

```
sam local invoke SeleniumFunction --docker-network samsele_s3_network
```

```
docker cp {container_name}:/tmp/screen.png ./
```
