#bin/sh
docker build -t web:latest .
docker stop flask-vue
docker rm flask-vue
docker run -d --name flask-vue -e "PORT=8765" -p 8007:8765 web:latest