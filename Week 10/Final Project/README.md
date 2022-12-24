# VerisiChat

#### Video Demo: https://youtu.be/v8ydC5OB1Os

#### Description:

VerisiChat is a real-time messaging platform that allows users to communicate with each other in private or group conversations. It has a simple and intuitive user interface, making it easy for users to send and receive messages, create and join groups, and manage their account settings.

To build VerisiChat, I wrote several Python scripts and HTML templates. Here's a brief overview of each file and what it contains:

application.py: This is the main script for the application. It defines the routes and functions for handling user requests and rendering templates. It also connects to the database and performs queries to store and retrieve data.

helpers.py: This script contains several helper functions that are used throughout the application. These include functions for formatting dates and currencies, sending email notifications, and validating user input.

templates/: This directory contains the HTML templates for the application. These templates use the Jinja2 template engine to insert dynamic data and generate the final HTML pages served to the user.

One of the main design choices I had to make was how to store and retrieve data from the database. I decided to use SQLite and the SQL module from the cs50 library, as it is lightweight and easy to use. I created three tables in the database: users, message_info, and messages. The users table stores information about the users, such as their username and password. The message_info table stores metadata about messages, such as the sender and recipient. And the messages table stores the actual message content.