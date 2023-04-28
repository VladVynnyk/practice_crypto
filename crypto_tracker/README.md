## For launching this project you need:

  1.Create docker container with command: `docker run -P -p 127.0.0.1:5433:5433 -e POSTGRES_PASSWORD="1234" --name tracker-db postgres:alpine`
  2.Install libraries from requirements.txt
  3.Run command: uvicorn main:app --reload
