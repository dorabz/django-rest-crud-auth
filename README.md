# web-lab1

DJANGO REST FRAMEWORK - CRUD & AUTH

database -SQLite

The built web service has TWO asset groups - users & recipes, that are mapped to the URL address. 
Web service has a URL for accessing recipes (eg /recipes/) and a URL for accessing user's profile (eg /users/). Additionally, it supports nested asset retrieval on at least one pair of funds - retrieval of all recipes of a specific user (eg /users/1/recipes/).
CRUD operations are available for users and recipies of particular user.

Implemented Token authentication and Session authentification for DRF web browser. 
The program interface is available at http://localhost:8000/api. 
The root URL http://localhost:8000/ contains documentation page in the form of a index.html page with a list of all URL addresses and all associated CRUD methods with short description. 

Implemented automated testing with APITestCase. For every exposed combination of URL address and HTTP method
was written at least one test case that enables checking services after modifying the program code.

How to start:


 - pip install -r requirements.txt
 - python manage.py makemigrations
 - python manage.py migrate
 - python manage.py runserver
 - python manage.py test
