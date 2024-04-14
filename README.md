# Bottle CRUD Operations Project

Welcome to the Bottle CRUD Operations Project! This is a web application built with Bottle, a micro web framework for Python, that performs CRUD (Create, Read, Update, Delete) operations using ArangoDB and SQLite3. The project allows admin users to manage data stored in ArangoDB, while admin user credentials are stored in a SQLite3 database.

## Description

The Bottle CRUD Operations Project provides a simple interface for admin users to perform CRUD operations on data stored in ArangoDB. Admin users can log in to the system using their credentials stored in the SQLite3 database. Once logged in, they can create, read, update, and delete records in the ArangoDB database. Additionally, the project includes functionality for sending confirmation emails to newly registered admin users.

## Features

- User Authentication: Admin users can log in to the system using their credentials stored in the SQLite3 database.
- CRUD Operations: Admin users can perform CRUD operations on data stored in ArangoDB, including creating, reading, updating, and deleting records.
- Data Management: The project provides a user-friendly interface for managing data, with forms and buttons for performing CRUD operations.
- Confirmation Emails: After signing up, admin users receive a confirmation email with a unique verification link to activate their account.
- Error Handling: The project includes error handling mechanisms to handle invalid inputs, database errors, and other potential issues.

## Technologies Used

- Python: Used for server-side logic and backend development.
- Bottle: A micro web framework for Python used to build the web application.
- ArangoDB: A distributed NoSQL database used to store and manage data.
- SQLite3: A lightweight relational database management system used to store admin user credentials.
- SMTP: Simple Mail Transfer Protocol used to send confirmation emails to admin users.
- JavaScript: Used for client-side scripting and dynamic behavior in the web application.

## Installation

1. Clone the repository to your local machine:
