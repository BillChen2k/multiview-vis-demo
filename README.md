# multiview-vis-demo

![2021-10-20-fKpOTG](https://billc.oss-cn-shanghai.aliyuncs.com/img/2021-10-20-fKpOTG.png)

## Local deployment

Make sure docker is properly installed, then:

```
docker build -t multiviewvis:latest .
docker run -d --name flask-vue -e "PORT=1234" -p 8007:1234 multiviewvis:latest
```

Where environment variable PORT is the port you want to exposed to the host machine.

## Auto deployment

Any push to the master branch will trigger GitHub CI, if passed, `Heroku` will redeploy the project with the newest Dockerfile and source code.

---

2021.10

East China Normal University
