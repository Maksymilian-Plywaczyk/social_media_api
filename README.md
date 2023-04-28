# SOCIAL MEDIA API

Hi! This project backend especially API project which can be used to create full stack social media web application. Using Django Rest Framework with Python.
</br>
The project is meant to be easily clone-able, and used as starter for the development of Social media API.

## Getting started

 1. Create directory for this project and go to this folder:\
  `mkdir <your_directory_name>`\
  `cd <your_directory_name>`
 2. Clone the repository from GitHub (using HTPS):\
	`git clone https://github.com/Maksymilian-Plywaczyk/social_media_api.git`
 3. Create a virtual environment to isolate our package dependencies locally\
	 `python -m venv venv`\
	 `source venv/bin/activate` or on Windows `venv/Scripts/activate`
 4. Install list of dependencies from `requirements.txt`\
	`pip install -r requirements.txt`
 5. Create `.env` file as the `.env.example` file and swap `SECRET KEY` with yours.
 6. Run `python manage.py makemigrations` for making migration, then run `python manage.py migrate`  to sync your database for the first time.
7. Run the project using `python manage.py runserver` and you should see the `Page not found` (but not worries this is correct behavior) page provided by Django at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
8. Feel free to use this API :)
	
## How to generate SECRET KEY for Django application

 1. Using a dedicated website:\
	 [Django SECRET KEY generator](https://djecrety.ir/)
 2. Using Django shell:\
  `python manage.py shell`\
	  Import the `get_random_secret_key()` function from `django.core.management.utils`:\
	  `from django.core.management.utils import get_random_secret_key`\
	  Generate the Secret Key in terminal:\
	  `print(get_random_secret_key())` and copy your Secret Key for `.env` file.
## How to use API (endpoints)
At the moment, the API provides 5 different endpoints. The application will be developed with further functionalities in the future. Below are examples of the use of each of the endpoints created. You can test endpoint using Postman.

 1.  **POST** **`api/register/`** public endpoint for register new user to application. We use two `user_type`: **normal** and **superuser**.

 **Request body**
	 
    {
	    "email":"your_email", 
	    "password":"your_password", 
	    "user_type":"normal"
    }
**Response body**

    {
	    "user":  
	    {
		    "id":  user_id,
		    "email": "your_email",
		    "password":  "hashed password"
	    },
	    "token":  "token"
    }

 2. **POST** **`api/login/`** public endpoint for log in user to application. 
 
 **Request body**
	 
    {
	    "username":"your_email", 
	    "password":"your_password",
    }
**Response body**

    {
		"expiry":  "date",
		"token":  "token"
    }

 3. **GET** **`api/posts/`** public endpoint for read list of Posts with comments associated with it.

**Response body**

    {
		{
			"count":  1,
			"next":  "http://localhost:8000/api/posts/?page=2",
			"previous":  null,
			"results":  [
				{
					"id":  1,
					"title":  "Post 1",
					"content":  "Content of post",
					"author_id":  1,
					"comments":  [
						{
							"id":  1,
							"content":  "Comment of Post 1",
							"created_at":  "2023-04-27T20:05:10.268118Z",
							"author_id":  1,
							"post_id":  1,
							"likes":  
								[
									1
								]
						}
					]
				}
			]
		}
	}
4. **POST** **`api/posts/create`** private endpoint only for superusers to create Post with associated with it comments. You need to pass `Authorization` in `headers` with value `Token <your_token_from_login_or_register>`

**Request body**
		
	{
		"title":"title"
		"content":"content post",
		"author_id":  1,
		"comments":  [
			{
					"content":  "Comment of Post 1",
					"created_at":  "2023-04-27T20:05:10.268118Z",
					"author_id":  2,
					"likes":  [
						1
					]
			},
			{
					"content":  "Comment2 of Post 1",
					"created_at":  "2023-04-27T20:05:10.268118Z",
					"author_id":  3,
					"likes":  [
						1,2,3
					]
			}

		]
	}
   

**Response body**

   	{
   
		"id":1,
		"title":"title",
		"content":"content post",
		"author_id":  1,
		"comments":  [
			{
					"id":  1,
					"content":  "Comment of Post 1",
					"created_at":  "2023-04-27T20:05:10.268118Z",
					"author_id":  2,
					"post_id":  1,
					"likes":  [
						1
					]
			},
			{
					"id":  2,
					"content":  "Comment2 of Post 1",
					"created_at":  "2023-04-27T20:05:10.268118Z",
					"author_id":  3,
					"post_id":  1,
					"likes":  [
						1,2,3
					]
			}

		]
	}
5. **PUT** **`api/posts/<int:pk>/update`** private endpoint only for owners to update Post with associated with it comments. You need to pass `Authorization` in `headers` with value `Token <your_token_from_login_or_register>`

**Request body**
		
	{
		"title":"title"
		"content":"content post",
		"author_id":  1,
		"comments":  [
			{
					"content":  "Comment of Post 1",
					"created_at":  "2023-04-27T20:05:10.268118Z",
					"author_id":  2,
					"likes":  [
						1
					]
			},
			{
					"content":  "Comment2 of Post 1",
					"created_at":  "2023-04-27T20:05:10.268118Z",
					"author_id":  3,
					"likes":  [
						1,2,3
					]
			}

		]
	}
   

**Response body**

   	{
   
		"id":1,
		"title":"title",
		"content":"content post",
		"author_id":  1,
		"comments":  [
			{
					"id":  1,
					"content":  "Comment of Post 1",
					"created_at":  "2023-04-27T20:05:10.268118Z",
					"author_id":  2,
					"post_id":  1,
					"likes":  [
						1
					]
			},
			{
					"id":  2,
					"content":  "Comment2 of Post 1",
					"created_at":  "2023-04-27T20:05:10.268118Z",
					"author_id":  3,
					"post_id":  1,
					"likes":  [
						1,2,3
					]
			}

		]
	}
## TODO
 **MODELS**
 - [x] Create 3-4 sample models (Here we got User, Post and Comment)
 - [x] at least one relation one-to-many between models
 - [x] at least one relation many-to-many between models
 - [x] custom User model with type field\
 **ENDPOINTS**
 - [x] Enpoint for register user using email, password and user_type
 - [x] Endpoint to log in by user
 - [x] public endpoint to serve data from your models with all related objects
 - [x] private endpoint (only for superusers) to create entry with nested objects
 - [x] private endpoint (only for owners) to update entry with nested objects
