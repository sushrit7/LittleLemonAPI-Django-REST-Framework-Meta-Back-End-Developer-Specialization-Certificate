# Little Lemon API - Django REST Framework Back-End Developer Specialization

## Introduction

This repository contains the back-end codebase for the Little Lemon restaurant API, developed as part of the Django REST Framework Back-End Developer Specialization Certificate. The API is designed to support various functionalities for managing menu items, orders, user roles, and more.

## Project Scope

The primary goal of this project is to create a robust API that enables client application developers to build web and mobile applications for the Little Lemon restaurant. The API supports user roles, menu item management, cart management, order processing, and user group management.

## Project Structure

The project is organized into a single Django app named `LittleLemonAPI`. Dependencies are managed using `pipenv`. Please review the [video tutorial](#) on creating a Django project using pipenv for setup instructions.

## Functionality and Views

You have the flexibility to use function-based or class-based views throughout the project. Follow the proper API naming conventions, as outlined in the [video tutorial](#) on naming conventions.

## User Groups

Two user groups, namely "Manager" and "Delivery Crew," have been created. Utilize the Django admin panel to assign users to these groups. Users not assigned to any group are considered customers. Refer to the [video tutorial](#) on user roles for more details.

## Error Handling and Status Codes

Ensure proper error handling by displaying error messages with appropriate HTTP status codes. Refer to the table below for the list of status codes and their corresponding reasons:

| HTTP Status Code | Reason                     |
| -----------------| -------------------------- |
| 200              | Ok                         |
| 201              | Created                    |
| 403              | Unauthorized               |
| 401              | Forbidden                  |
| 400              | Bad Request                |
| 404              | Not Found                  |

## API Endpoints

### User Registration and Token Generation

- **POST /api/users**
  - Role: No role required
  - Purpose: Creates a new user with name, email, and password.

- **GET /api/users/me/**
  - Role: Anyone with a valid user token
  - Purpose: Displays only the current user.

- **POST /token/login/**
  - Role: Anyone with a valid username and password
  - Purpose: Generates access tokens for use in other API calls.

### Menu Items

#### Accessible by Customers and Delivery Crew

- **GET /api/menu-items**
  - Purpose: Lists all menu items.

- **GET /api/menu-items/{menuItem}**
  - Purpose: Lists a single menu item.

#### Accessible by Managers

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

### User Group Management

#### Manager Only

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

### Cart Management

#### Accessible by Customers

- **GET /api/cart/menu-items**
  - Purpose: Returns current items in the cart.

- **POST /api/cart/menu-items**
  - Purpose: Adds a menu item to the cart.

- **DELETE /api/cart/menu-items**
  - Purpose: Deletes all menu items in the cart.

### Order Management

#### Accessible by Customers

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

#### Accessible by Managers

- **GET /api/orders**
  - Purpose: Returns all orders with order items.

- **GET /api/orders/{orderId}**
  - Purpose: Returns all items for a specific order.

- **DELETE /api/orders/{orderId}**
  - Purpose: Deletes an order.

#### Accessible by Delivery Crew

- **GET /api/orders**
  - Purpose: Returns all orders with order items assigned to the delivery crew.

- **PATCH /api/orders/{orderId}**
  - Purpose: Updates the order status.

### Additional Steps

Implement proper filtering, pagination, and sorting for `/api/menu-items` and `/api/orders` endpoints. Refer to the [videos](#) on filtering, searching, and pagination, as well as the [reading](#) on more filtering and pagination.

### Throttling

Apply throttling for both authenticated and anonymous/unauthenticated users. Review the [video tutorial](#) and the [reading](#) on API throttling for guidance.

## Conclusion

With a comprehensive understanding of the project scope and essential API endpoints, you are now well-equipped to embark on the development journey. Good luck, and happy coding!
