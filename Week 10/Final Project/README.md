# VerisiChat
#### Video Demo: https://youtu.be/v8ydC5OB1Os
#### Description:
VerisiChat is a real-time messaging platform that allows users to communicate with each other in private or group conversations. It has a simple and intuitive user interface, making it easy for users to send and receive messages, create and join groups, and manage their account settings.

To build VerisiChat, the following Python scripts and HTML templates were used:

* application.py:
    * Main script for the application
    * Defines routes and functions for handling user requests and rendering templates
    * Connects to the database and performs queries to store and retrieve data
* helpers.py:
    * Contains helper functions used throughout the application
    * Functions include formatting dates and currencies, sending email notifications, and validating user input
* templates/:
    * Contains HTML templates for the application
    * Uses Jinja2 template engine to insert dynamic data and generate final HTML pages served to the user

One of the main design choices I had to make was how to store and retrieve data from the database. I decided to use SQLite and the SQL module from the cs50 library, as it is lightweight and easy to use. I created three tables in the database: users, message_info, and messages. The users table stores information about the users, such as their username and password. The message_info table stores metadata about messages, such as the sender and recipient. And the messages table stores the actual message content.

Another design choice I had to make was how to implement real-time messaging. I decided to use WebSockets and the Flask-SocketIO extension to allow the server and client to communicate in real-time. This allows messages to be sent and received instantly, without the need for the user to refresh the page.

I also implemented several security measures to ensure the safety and privacy of the users. These include hash and salt password storage, secure cookies for maintaining user sessions, and input validation to prevent SQL injection attacks.

In addition to messaging, I also added several other features to enhance the user experience. These include the ability to create and join groups, view and update user profiles, and view a history of past messages.

VerisiChat is a well-designed messaging platform that offers users a simple and intuitive interface for communicating with each other in real-time. With its robust security measures and additional features, VerisiChat provides users with a safe and enjoyable experience.