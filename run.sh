docker build . -t quay.io/agcdev0/major-project:latest
docker push quay.io/agcdev0/major-project:latest
uvicorn main:app --reload
