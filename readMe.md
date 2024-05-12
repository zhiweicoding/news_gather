# news load 
## 1. 部署方式

```shell
docker build -t loveqianqian/news_gather:main .
```

```shell
docker run -d -p 9080:9080 loveqianqian/news_gather:main
```

docker-compose.yml
```docker
version: '3.8'

services:
  fastapi-app:
    image: loveqianqian/news_gather:main
    container_name: new_gather
    ports:
      - "9080:9080"
    environment:
      - MODULE_NAME=main 
      - VARIABLE_NAME=app
    restart: always  
```