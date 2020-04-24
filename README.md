# prog-image
REST API service to upload, process and download images.
The system is a demonstration of a microservice architecture that is fully scalable to accept a very high volume of requests.

## Architecture
The motivation for the project was to build a scalable image processing API. The archecture is built of microservices, each designed to process an image. The services are built using [nameko](https://nameko.readthedocs.io/en/stable/) using [RabbitMQ](https://www.rabbitmq.com/) as the AMPQ messaging broker. Images are stored in [MongoDB](https://www.mongodb.com/) making use of [GridFS](https://docs.mongodb.com/manual/core/gridfs/) file storage.

There is a single HTTP service which acts as the external facing interface to the system. It's designed to be lightweight and ship the processing off to the subsequest service. The current selection of services consist of an image upload service and image processing services for JPEG conversion, PNG conversion, Grayscale filtering and image flipping.

There should always be a single instance of the HTTP API service running, but the processing services are scalable so many can run at the same time. In a production environment, the system can be placed infront of a load balancer to enable more HTTP API services to be running.

## API Docs
`POST /upload_file` - Uploads an image returning the `image_id` in the response

Curl example:
```bash
curl --location --request POST 'localhost:8000/upload_file' \
--header 'Content-Type: multipart/form-data; boundary=--------------------------331539197270314924163946' \
--form 'image=@/sample_image.png'
```
`GET /<image_id>/jpeg` - Returns the image in jpeg format

`GET /<image_id>/png` - Returns the image in png format

`GET /<image_id>/grayscale` - Returns the image in grayscale

`GET /<image_id>/mirror` - Returns the image flipped left-to-right

## Installation
The project is fully dockerized with containers for RabbitMQ, MongoDB, api-service and each of the image processing services. Run
```bash
docker-compose up -d
```
to start all services. The main http api will be available on `localhost:8000`

## Testing
Tests are ran using [pytest](https://docs.pytest.org/en/latest/). To run the tests, make sure you have all requirements installed. It's recomended to use a `venv` for this.
```bash
pip install virtualenv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
To run the tests, from the `prog_image` directory, run:
```
python -m pytest
```
You must also have the mongo and rabbitmq docker containers running.
