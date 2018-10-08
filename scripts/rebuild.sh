docker build -t harvest-api .
#
#rm all stopped containers
#docker ps -aq --no-trunc -f status=exited | xargs docker rm
#
#rm all stopped images
docker rmi $(docker images -f "dangling=true" -q)
docker-compose up
