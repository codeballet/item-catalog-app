# Item catalog

The *Item Catalog* is a full-stack web app with a HTML interface and an API. The web app allows for loggin in as a registered user. Once logged in, the user can add, edit, and delete categories, as well as items for each category. Non-logged in users can still browse and access all items and categories, but they cannot edit, delete, or add new categories or items. 

## Installation and configuration of linux virtual machine
To run the program, you can ssh into a virtual machine, which is pre-configured in a Vagrant file. To do so, you first need to install the following software:
* [Git](https://git-scm.com/downloads)
* [Virtualbox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)

To get the Vagrant configuration file of the Virtual Machine, fork and clone the following repository:
* https://github.com/udacity/fullstack-nanodegree-vm

Inside the cloned directory, there is a `vagrant` directory. Change directory to that `vagrant` directory and run the command `vagrant up`.
Once the virtual machine configuration has finished its work, you may connect via SSH to the virtual machine with the command `vagrant ssh`.
When you see a shell prompt starting with the word `vagrant`, you have successfully logged into the virtual machine.

Inside the virtual machine, change directory to `/vagrant`. That directory is shared with your host operative system. Inside the `/vagrant` directory, download or clone the files from the following github repository:
* `https://github.com/codeballet/item-catalog.git`

### OAuth and session data
In order to log on and start a user session, you need to create two files:
* `client_secrets.json` containing your Google OAuth `client_id` and `client_secret`.
* `session_secrets.json` containing your a key `secret` to be used by Flask to create a session.

In order to generate the Google OAuth `client_secrets.json` file, you need to:
* Log on at `https://console.developers.google.com/apis/credentials`.
* Create an `OAuth 2.0 client ID`.
* Specify relevant `Authorised JavaScript origins` (i.e. `http://localhost:8000`) and `Authorised redirect URIs` (i.e. `http://localhost:8000/oauth/google`)
* Download the JSON file, name it `client_secrets.json`, and put in the root directory of the app.

To generate the `session_secrets.json` file:
* Create a file called `session_secrets.json`.
* Inside the file, there should be a JSON formatted string with a key that is named `secret`. The value can be any random value of digits and letters. For instance, `{"secret": "YOUR_RANDOM_SECRET_SESSION_KEY"}`.
* Put the file in the root directory of the app.

Below is an example of how you may create the `session_secrets.json` file in python:
```
import os
import base64
import json
random_bytes=os.urandom(64)
data=base64.b64encode(random_bytes).decode('utf-8')
data_dic={}
data_dic['secret']=data
with open('session_secrets.json','w') as f:
    json.dump(data_dic,f)
```

### Starting the server and using the app
Once all above installations and configurations are done, change directory to the root of the app and `python application.py`. The server should now be up and running, and the list of categores in the database available at the URL`http://localhost:8000/` and `http://localhost:8000/catalog`.

### Requirements for custom installation
In case you do not want to use the preconfigured Vagrant file and Virtualbox, all dependencies are listed in the file `requirements.txt`. To install all the requirements in your own custom linux configuration, run the command `pip install -r requirements.txt`

## Loggin in on the HTML website
### Create a new user and login on the webpage
On the HTML web interface, the only option for logging in is by means of Google's OAuth 2.0 service. To log in and register as a user on the `http://localhost:8000/login` page, simply click on the Google `Sign In` button.

In case you have never logged on before, a new user will be created, collecting your Google user account name and email information. Once logged on, the website will display a welcome page that includes a temporary token, which you may use to access the API.

## Using the API
### Creating new user and login with the API
To access the API, you may use a tool such as `curl`. To create a new user, you need to submit a `name`, `email`, and `password` to the API endpoint `/api/users`. For instance:
```
curl -H "Content-Type: application/json" -d '{"name":"YOUR_NAME","email":"YOUR_EMAIL","password":"YOUR_PASSWORD"}' http://localhost:8000/api/users
```
Having created a user, you may access the API, providing the `name` and `password` information. Altearnatively, you may use the temporary token displayed at the HTML login page, upon a successful OAuth login.

### API Resources available without login
There are three API endpoints available for a non-logged in user:
* `/api/users` to create new users (as above).
* `/api/catalog/categories` to get a json response with all existing categories in the database.
* `/api/catalog/items` to get a json response with all existing items in the database.

For instance, you may acquire all categories like so:
```
curl http://localhost:8000/api/catalog/categories
```

### API calls as a logged in user
You may log in with username and password, such as `curl -u YOUR_NAME:YOUR_PASSWORD`. Alternatively, you may use a temporary token. The token can be acquired in two ways.

The first way to acquire a temporary token is to login on the HTML webpage, using the Google Sign in button. Upon logging in, a temporary token will be displayed on the successful login page.

The second way is to create a user account over the API (as described above), and then send a request to the `/api/token` endpoint. For instance:
```
curl -u YOUR_NAME:YOUR_PASSWORD http://localhost:8000/api/token
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
 curl -X POST -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"name":"CATEGORY_NAME"}' http://localhost:8000/api/catalog/category
```

#### Viewing a category with `GET`
In order to view a category, you need to send a `GET` request with the category `id` of the relevant category, such as:
```
curl -X GET -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID"}' http://localhost:8000/api/catalog/category
```

#### Editing a category with `PUT`
To edit a category, you send a `PUT` request, containing the category `id` and `name`. For instance:
```
 curl -X PUT -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID","name":"NEW_CATEGORY_NAME"}' http://localhost:8000/api/catalog/category
```

#### Deleting a category with `DELETE`
To delete a category, you send a `DELETE` request, containing the category `id`, such as:
```
 curl -X DELETE -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID"}' http://localhost:8000/api/catalog/category
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
curl -X POST -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"category_id":"ID","name":"ITEM_NAME","price":"PRICE","description":"SOME_DESCRIPTION"}' http://localhost:8000/api/catalog/item
```

#### Viewing an item with `GET`
To view an item, your own or an item belonging to another user, you may send a `GET` request with the relevant item `id`. Example of request:
```
curl -X GET -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID"}' http://localhost:8000/api/catalog/item
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
curl -X PUT -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID","name":"NEW_ITEM_NAME"}' http://localhost:8000/api/catalog/item
```

#### Deleting an item with `DELETE`
To delete an item, you send a `DELETE` request containing the `id` of the item. The request may look like:
```
curl -X PUT -H "Content-Type: application/json" -u YOUR_NAME:YOUR_PASSWORD -d '{"id":"ID"}' http://localhost:8000/api/catalog/item
```

## Contributions
The software is currently a course project, as part of the "Full Stack Web Developer Nanodegree Program" by Udacity. As a course project, it is currently not open to contributions.

I am planning in the future to develop the project into a production release, at which point the code may be opened for contributions.

## Licensing
All intellectual property belongs to Johan Stjernholm. Please contact Johan Stjernholm for any requests to use the code.