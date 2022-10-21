# bioweb-api
A RESTFUL web service built using django models. The dataset is a mock set of protein domains data in csv format. Database built using SQLite3. This project explores the django serializations and modelling cretaing appropriate relations with the various attributes present in the dataset. Upon creation of the models, data will be inserted them through a script 'load_data.py'. 

The API views are set up using Django Rest Framework (DRF). Serializers objects are created corresponding to each django model, with a few additional serializers that cater for unique API views. The views are mainly built using function based views (@api_view([method_names]). These views are then linked with a url for the browser to render the page.

There are a total of 6 endpoints:
1. POST http://127.0.0.1:8000/api/protein/ - add a new record
2. GET http://127.0.0.1:8000/api/protein/[PROTEIN ID] - return the protein sequence and all we know about it
3. GET http://127.0.0.1:8000/api/pfam/[PFAM ID] - return the domain and it's description
4. GET http://127.0.0.1:8000/api/proteins/[TAXA ID] - return a list of all proteins for a given organism
5. GET http://127.0.0.1:8000/api/pfams/[TAXA ID] - return a list of all domains in all the proteins for a given organism.
6. GET http://127.0.0.1:8000/api/coverage/[PROTEIN ID] - return the domain coverage for a given protein

API view of ENDPOINT (2):
     
A series of unit tests using DjangoModelFactory and APITestCase packages to ensure the successful creations/populations of objects and routes.

## Initialize project
* `django-admin startproject bioweb`
* `cd bioweb`
* `python manage.py startapp proteins`

### To run tests:
* cd to bioweb directory and enter the command: 
* `python manage.py test`

### To run the data loading script: 
* cd to bioweb/proteins directory and enter the command: 
* `python scripts/load_data.py`
