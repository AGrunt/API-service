# API-service
 Coffee selection rest api service

## Requirements
* docker engine installed

## How to run

* Run `docker compose up`

## How to use

Service available at `http://localhost:5001`  
Documentation for available methods accessable at `http://localhost:5001/swagger`  

Swagger interface allow to try out methods and get service response.  
To try out methods through swagger UI press `Try it out`, fill required fields, and press `Execute` button bellow  

Every response is hardcoded now for test reasons.

## References

### ./docs folder content

* mock_users.csv - list of user's ids for text purposes. Hardcoded in flask api application for responces at `/users/<id>/recommendations` (GET), `/users/<id>` (GET;PUT), `/users/<id>/responses` (PUT'), `/users/<id>/rankings/<cafeid>` (PUT).
* answers_option.csv - expected answers' options for user's questionare
* questionare_questions.csv - expected to recieve through `/users/<id>/responses` (PUT')
* coffee_mate_mock_data.xlsx - initial dataset for database poppulation

### ./docs/generated folder content

* cafes.csv - list of cafes
* reviews.csv - list of reviews

### ./scripts folder content

* scripts/V001_coffee_mate.sql - version 001 of initializing script for mysql container. Database schema only. 
* scripts/V002_coffee_mate.sql - version 002 of initializing script for mysql container. Contain all data scrapped from Google Maps API.

### ./static folder content

* swagger.json - config file of API service swagger documentation

### ./templates folder content

TemplateS for flask application. Home page.

## Notes

* update api-app.py:
  `docker cp ./api-app.py api-svc:/app/ ; docker container restart api-svc`

* update sql volume with latest sql script or rewrite spoiled schema:
  1. delete mysql container and its volume:
    `docker stop api-db ; docker rm api-db ; docker volume rm api-service_api-db`
  2. rebuild container
    `docker compose up --build`
    
docker ps -a | grep "api-db" | awk '{print $1}' | xargs docker rm


* Functions:

  * Get user
    GET /users/{id}
    Status: ready

  * Add user
    PUT /users/{id}
    Status: ready

  * Get recommendations
    GET /users/{id}/recommendations
    Status: InProgress

  * User's answers collection
    PUT /users/{id}/responses
    Status: ready

  * User's cafe ranking collection
    PUT /users/{id}/rankings/{cafeid} 
    Status: ready