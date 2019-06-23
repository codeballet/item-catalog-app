# Item catalog
The *Item Catalog* is a database driven web app that stores items organized in different categories.

As of 23 June 2019, an instance of the app is running at [spaceengineering.biz](https://spaceengineering.biz/catalog). That domain is using an SLL/TLC encryption by Let's Encrypt for HTTPS access.

The *Item Catalog* can be accessed via a HTML interface and an API. The app allows for loggin in as a registered user. Once logged in, the user can add, edit, and delete categories, as well as items for each category. Non-logged in users can still browse and access all items and categories, but they cannot edit, delete, or add new categories or items. 

## Installation and configuration
The github repository is designed to be directly cloned into a server running Ubuntu, Apache, and PostgreSQL. All file paths in the code are relative, so hardly any configuration of the actual code is necessary.

However, in order to work, you need to provide the following:
* A `client_secrets.json` file containing your Google OAuth information.
* A `SECRET_KEY` environment variable that can be accessed by Apache.
* A `DATABASE_URL` environment variable that can be accessed by Apache.

### Generating the OAuth file `client_secrets.json` from Google
In order to generate the Google OAuth `client_secrets.json` file, you need to:
* Log on at `https://console.developers.google.com/apis/credentials`.
* Create an `OAuth 2.0 client ID`.
* Specify relevant `Authorised JavaScript origins` (i.e. `http://localhost:8000`) and `Authorised redirect URIs` (i.e. `http://localhost:8000/oauth/google`)
* Download the JSON file, name it `client_secrets.json`, and put in the root directory of the app.

### Generating the `SECRET_KEY`
Below is an example of how you may create the `SECRET_KEY` variable in python (the last line decoding the key to utf-8):
```
import os
import base64
import json
random_bytes=os.urandom(64)
data=base64.b64encode(random_bytes).decode('utf-8')
```

### The `DATABASE_URL`
The `DATABASE_URL` variable should have the following formula, if usign PostgreSQL:
```
postgresql://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME
```

### Installing app dependencies
All dependencies for the app are listed in the file `requirements.txt`. To install all the requirements, run the command `pip install -r requirements.txt`

## Loggin in on the HTML website
### Create a new user and login on the webpage
On the HTML web interface, the only option for logging in is by means of Google's OAuth 2.0 service. To log in and register as a user, simply click on the Google `Sign In` button on the login page.

In case you have never logged on before, a new user will be created, collecting your Google user account name and email information. Once logged on, the website will display a welcome page that includes a temporary token, which you may use to access the API.

## Using the API
In the below examples, it is assumed that you are accessing the API locally. If you are accessing the app as a production website, the API needs to be accessed with whichever domain name or IP address you have given your website.

For instance, as of 23 June 2019, an api call to get the item categories would look like:
```
curl https://spaceengineering.biz/api/catalog/categories
```

### Creating new user and login with the API
To access the API, you may use a tool such as `curl`. To create a new user, you need to submit a `name`, `email`, and `password` to the API endpoint `/api/users`. For instance:
```
curl -H "Content-Type: application/json" -d '{"name":"YOUR_NAME","email":"YOUR_EMAIL","password":"YOUR_PASSWORD"}' http://localhost:80/api/users
```
Having created a user, you may access the API, providing the `name` and `password` information. Altearnatively, you may use the temporary token displayed at the HTML login page, upon a successful OAuth login.

### API Resources available without login
There are three API endpoints available for a non-logged in user:
* `/api/users` to create new users (as above).
* `/api/catalog/categories` to get a json response with all existing categories in the database.
* `/api/catalog/items` to get a json response with all existing items in the database.

For instance, you may acquire all categories like so:
```
curl http://localhost:80/api/catalog/categories
```

### API calls as a logged in user
You may log in with username and password, such as `curl -u YOUR_NAME:YOUR_PASSWORD`. Alternatively, you may use a temporary token. The token can be acquired in two ways.

The first way to acquire a temporary token is to login on the HTML webpage, using the Google Sign in button. Upon logging in, a temporary token will be displayed on the successful login page.

The second way is to create a user account over the API (as described above), and then send a request to the `/api/token` endpoint. For instance:
```
curl -u YOUR_NAME:YOUR_PASSWORD http://localhost:80/api/token
```
The json response will contain a token as such:
```
{"token":"SOME_TOKEN_CODE"}
```
ONce the token is received, it may be used for further requests, instead of entering the username and password. When using a token, you enter the token in the place of the `name` field, and any value may be entered in the the password field, for instance `curl -u YOUR_TOKEN:BLANK`.

### Operating on categories with the API
As a logged in user, you may view any category. You may add new categies, and you may edit and delete your own categores. The API endpoint for operating on categories is:
```
/api/catalog/category
```

#### Adding a category with `POST`
To add a category, you need to send a `POST` request to the above API endpoint. The request must have a category `name` specified. For instance:
```
 curl -X POST -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"name":"CATEGORY_NAME"}' http://localhost:80/api/catalog/category
```

#### Viewing a category with `GET`
In order to view a category, you need to send a `GET` request with the category `id` of the relevant category, such as:
```
curl -X GET -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID"}' http://localhost:80/api/catalog/category
```

#### Editing a category with `PUT`
To edit a category, you send a `PUT` request, containing the category `id` and `name`. For instance:
```
 curl -X PUT -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID","name":"NEW_CATEGORY_NAME"}' http://localhost:80/api/catalog/category
```

#### Deleting a category with `DELETE`
To delete a category, you send a `DELETE` request, containing the category `id`, such as:
```
 curl -X DELETE -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID"}' http://localhost:80/api/catalog/category
```

### Operating on items with the API
As a logged in user, you may view any item in the database. You may also create, edit, and delete items in your own categories. You may not create, edit, or delete items in other users categories.

The API endpoint for operating on items is:
```
/api/catalog/item
```

#### Adding an item to a category with `POST`
To add an item to a category, you send a `POST` request. The request must contain the following data:
* `category_id` for the category you want the item to belong to.
* `name` of the item.
You may only add items to your own categories.

Optional pieces of information that may be provided about the item are:
* `price`
* `description` giving more details about the item.
The request may look like this:
```
curl -X POST -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"category_id":"ID","name":"ITEM_NAME","price":"PRICE","description":"SOME_DESCRIPTION"}' http://localhost:80/api/catalog/item
```

#### Viewing an item with `GET`
To view an item, your own or an item belonging to another user, you may send a `GET` request with the relevant item `id`. Example of request:
```
curl -X GET -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID"}' http://localhost:80/api/catalog/item
```

#### Editing an item with `PUT`
To edit an item, you send a `PUT` request containing the data you want to edit.

Compulsory data:
* `id` for the item.
Optional data, depending on what you want to edit:
* `category_id`, which must be your own category.
* `name` of item.
* `price` of item.
* `description` of item.
The request may look like this:
```
curl -X PUT -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID","name":"NEW_ITEM_NAME"}' http://localhost:80/api/catalog/item
```

#### Deleting an item with `DELETE`
To delete an item, you send a `DELETE` request containing the `id` of the item. The request may look like:
```
curl -X PUT -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID"}' http://localhost:80/api/catalog/item
```

## Contributions
The software is currently a course project, as part of the "Full Stack Web Developer Nanodegree Program" by Udacity. As a course project, it is currently not open to contributions.

I am planning in the future to develop the project into a production release, at which point the code may be opened for contributions.

## Licensing
All intellectual property belongs to Johan Stjernholm. Please contact Johan Stjernholm for any requests to use the code.