# Build a website selling laptops with chatbox realtime using django Framework

## Team Dev ( 1 people )

- Thái Ngọc Quý | Admin | 0342280638

## Struture of Project  ( main file/package struture ) 

```
Home/
---Templates/
---models.py
---views.py

Mysite/
---asgi.py
---consumers.py
---routing.py
---settings.py
---urls.py

static/
```
1. **Home/**: This is the folder that contains necessary components such as models, views, and templates to perform specific functions in the project.
   - **Templates/**: This is the directory that contains the website's user interfaces.
   - **models.py**:  This file contains data tables in the database, each class contains attributes (fields) corresponding to columns in the table and methods related to the data.
   - **views.py**:  this file interacts with the database through models, and return responses to users through APIs with specific paths

2. **Mysite/**: This folder contains configuration files and settings for the entire Django project ( database , static files , host , MIDDLEWARE , Websocket ,.... ).
   - **asgi.py**: Similar to **'wsgi.py'** , this file provides an entry point for ASGI-compliant web servers that support asynchronous protocols such as WebSockets. It is often used for    
     applications that need real-time processing.
   - **consumers.py**: Define a WebSocket consumer for your chat application in Django, using Django Channels to handle real-time communication. Specifically, it creates a consumer for a 
     chat room, where users can send and receive text and image messages.
   - **routing.py**: Defines URL patterns for WebSocket connections in your Django application. It maps URLs to the WebSocket consumer you defined (ChatConsumer).
   - **setting.py**: Configuration for the program.
   - **urls.py**: Contains paths for each specific task of the program.

3. **static/**: This folder contains static files such as images, gifs, css and javascript files.

## I. Overall this applications 
- UI: Bootstrap, HTML, CSS and Javascript.
- Back End: using Django Framework to build website - language Python.
- Database: MySQL (Xampp).

## II. Demo Main features of the program 
1. Order, view cart, view detailed product information ( Customer ).

3. Sign in and register an account with security supported by Django.
4. Chat with Admin/Manager.
   

