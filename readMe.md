# news gather

## 1. 部署

### 本地打包

```shell
docker build -t loveqianqian/news_gather:main .
```

```shell
docker run -d -p 9080:9080 loveqianqian/news_gather:main
```

#### docker-compose
start.yml
```yaml
version: "3.1"
services:
  news_gather:
    image: loveqianqian/news_gather:main
    container_name: news_gather
    ports:
      - "9080:9080"
    restart: always
    networks:
      - newsgather-network
    environment:
      - COS_SECRET_ID={{your secret id}}
      - COS_SECRET_KEY={{your secret key}}
      - COS_ENDPOINT={{your endpoint}}
      - COS_BUCKET={{your bucket name}}
      - COS_CDN_URL={{your cdn url}}
networks:
  newsgather-network:
    driver: bridge
```