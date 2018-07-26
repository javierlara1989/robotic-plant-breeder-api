docker build -t harvest-api .
docker rmi $(docker images -f "dangling=true" -q)
docker-compose up -d
