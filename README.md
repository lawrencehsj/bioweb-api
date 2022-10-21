# About the project
A RESTFUL web service built using django models. The dataset is a mock set of protein domains data in csv format. Database built using SQLite3. This project explores the django serializations and modelling cretaing appropriate relations with the various attributes present in the dataset. Upon creation of the models, data will be inserted them through a script 'load_data.py'. 

The API views are set up using Django Rest Framework (DRF). Serializers objects are created corresponding to each django model, with a few additional serializers that cater for unique API views. The views are mainly built using function based views (@api_view([method_names]). These views are then linked with a url for the browser to render the page.

### Features
There are a total of 6 endpoints:
1. POST http://127.0.0.1:8000/api/protein/ - add a new record
2. GET http://127.0.0.1:8000/api/protein/[PROTEIN ID] - return the protein sequence and all we know about it
3. GET http://127.0.0.1:8000/api/pfam/[PFAM ID] - return the domain and it's description
4. GET http://127.0.0.1:8000/api/proteins/[TAXA ID] - return a list of all proteins for a given organism
5. GET http://127.0.0.1:8000/api/pfams/[TAXA ID] - return a list of all domains in all the proteins for a given organism.
6. GET http://127.0.0.1:8000/api/coverage/[PROTEIN ID] - return the domain coverage for a given protein

Example API view of ENDPOINT (2):

![image](https://user-images.githubusercontent.com/58553029/197093496-4f4ddda7-e7ed-4efd-b0f4-91415a6e235c.png)

A series of unit tests using DjangoModelFactory and APITestCase packages to ensure the successful creations/populations of objects and routes.


### Built With
* Django
* sqlite


## Getting Started
Follow these instructions to get a local copy of this project up and running.

### Prerequisites
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation
Initialize the project in the Django environment through a series of commands that automatically creates the set of packages and files required to construct the app:

1. Clone the repo
   ```sh
   git clone [https://github.com/your_username_/Project-Name.git](https://github.com/lawrencehsj/bioweb-api.git)
   ```
2. Install NPM packages
   ```sh
   npm install
   ```
3. Start the django environment
   ```sh
   django-admin startproject bioweb 
   cd bioweb
   python manage.py startapp proteins
   ```
   
To run the script to populate the django models using the mock set of data:
```sh
cd bioweb/proteins
python scripts/load_data.py
```

To run the unit tests:
```sh
cd bioweb
python manage.py test
```
