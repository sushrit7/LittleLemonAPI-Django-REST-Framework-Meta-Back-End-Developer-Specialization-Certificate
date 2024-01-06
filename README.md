# Little Lemon API - Django REST-Framework, Back-End Developer Specialization

# Index
1. [Introduction](#introduction)
2. [Project Scope](#project-scope)
3. [Project Structure](#project-structure)
5. [User Groups](#user-groups)
7. [API Endpoints](#api-endpoints)
    1. [User Registration and Token Generation](#user-registration-and-token-generation)
    2. [Menu Items](#menu-items)
    3. [User Group Management](#user-group-management)
    4. [Cart Management](#cart-management)
    5. [Order Management](#order-management)
    6. [Additional](#additional)
    7. [Throttling](#throttling)
8. [Error Handling and Status Codes](#error-handling-and-status-codes)
9. [Getting Started](#getting-started)
    1. [Prerequisites](#prerequisites)
    2. [Clone the Repository](#clone-the-repository)
    3. [Set Up Virtual Environment and Install Dependencies](#set-up-virtual-environment-and-install-dependencies)
    4. [Run Migrations](#run-migrations)
    5. [Run the Development Server](#run-the-development-server)
10. [Conclusion](#conclusion)

## Introduction

This repository contains the back-end codebase for the Little Lemon restaurant API, developed as part of the Django REST Framework Back-End Developer Specialization Certificate. The API is designed to support various functionalities for managing menu items, cart, orders, user roles, and more.

## Project Scope

The primary goal of this project is to create a robust API that enables client application developers to build web and mobile applications for the Little Lemon restaurant. The API supports user roles, menu item management, cart management, order processing, and user group management.

## Project Structure

The project is organized into a single Django app named `LittleLemonAPI`. Dependencies are managed using `pipenv`. 

## User Groups

Two user groups, namely "Manager" and "Delivery Crew," have been created. Utilize the Django admin panel to assign users to these groups. Users not assigned to any group are considered customers. 

## API Endpoints

### 1. User Registration and Token Generation

- **POST /api/users**
  - Role: No role required
  - Purpose: Creates a new user with name, email, and password.

- **GET /api/users/me/**
  - Role: Anyone with a valid user token
  - Purpose: Displays only the current user.

- **POST /token/login/**
  - Role: Anyone with a valid username and password
  - Purpose: Generates access tokens for use in other API calls.

### 2. Menu Items

#### i. Accessible by Customers and Delivery Crew

- **GET /api/menu-items**
  - Purpose: Lists all menu items.

- **GET /api/menu-items/{menuItem}**
  - Purpose: Lists a single menu item.

#### ii. Accessible by Managers

- **GET /api/menu-items**
  - Purpose: Lists all menu items.

- **POST /api/menu-items**
  - Purpose: Creates a new menu item.

- **GET /api/menu-items/{menuItem}**
  - Purpose: Lists a single menu item.

- **PUT/PATCH /api/menu-items/{menuItem}**
  - Purpose: Updates a single menu item.

- **DELETE /api/menu-items/{menuItem}**
  - Purpose: Deletes a menu item.

### 3. User Group Management

#### i. Manager Only

- **GET /api/groups/manager/users**
  - Purpose: Returns all managers.

- **POST /api/groups/manager/users**
  - Purpose: Assigns a user to the manager group.

- **DELETE /api/groups/manager/users/{userId}**
  - Purpose: Removes a user from the manager group.

- **GET /api/groups/delivery-crew/users**
  - Purpose: Returns all delivery crew.

- **POST /api/groups/delivery-crew/users**
  - Purpose: Assigns a user to the delivery crew group.

- **DELETE /api/groups/delivery-crew/users/{userId}**
  - Purpose: Removes a user from the delivery crew group.

### 4. Cart Management

#### i. Accessible by Customers

- **GET /api/cart/menu-items**
  - Purpose: Returns current items in the cart.

- **POST /api/cart/menu-items**
  - Purpose: Adds a menu item to the cart.

- **DELETE /api/cart/menu-items**
  - Purpose: Deletes all menu items in the cart.

### 5. Order Management

#### i. Accessible by Customers

- **GET /api/orders**
  - Purpose: Returns all orders with order items.

- **POST /api/orders**
  - Purpose: Creates a new order item, adds items from the cart, and clears the cart.

- **GET /api/orders/{orderId}**
  - Purpose: Returns all items for a specific order.

- **PUT/PATCH /api/orders/{orderId}**
  - Purpose: Updates the order status and assigns a delivery crew.

- **DELETE /api/orders/{orderId}**
  - Purpose: Deletes an order.

#### ii. Accessible by Managers

- **GET /api/orders**
  - Purpose: Returns all orders with order items.

- **GET /api/orders/{orderId}**
  - Purpose: Returns all items for a specific order.

- **DELETE /api/orders/{orderId}**
  - Purpose: Deletes an order.

#### iii. Accessible by Delivery Crew

- **GET /api/orders**
  - Purpose: Returns all orders with order items assigned to the delivery crew.

- **PATCH /api/orders/{orderId}**
  - Purpose: Updates the order status.

### Additional

Filtering, pagination, and sorting are added at `/api/menu-items` and `/api/orders` endpoints.

## Error Handling and Status Codes

Refer to the table below for the list of status codes and their corresponding reasons:

| HTTP Status Code | Reason                     |
| -----------------| -------------------------- |
| 200              | Ok                         |
| 201              | Created                    |
| 403              | Unauthorized               |
| 401              | Forbidden                  |
| 400              | Bad Request                |
| 404              | Not Found                  |


## Getting Started

To get started with this project, follow the steps below:

### Prerequisites

- [Python](https://www.python.org/downloads/)
- [pipenv](https://pipenv.pypa.io/en/latest/installation.html)

### Clone the Repository

```bash
git clone https://github.com/your-username/LittleLemonAPI.git
```

cd LittleLemonAPI
### Set Up Virtual Environment and Install Dependencies
```bash

pipenv install
pipenv shell
```
### Run Migrations
```bash

python manage.py makemigrations
python manage.py migrate

```
### Run the Development Server
```bash
python manage.py runserver
```
Now, you can access the API at http://127.0.0.1:8000/.

## Conclusion

With a comprehensive understanding of the project scope and essential API endpoints, you are now well-equipped to embark on the development journey. Good luck, and happy coding!
