# E-commerce System with Shopping Cart

## Overview
This project is a backend API that simulates a simple e-commerce platform.  
It allows users to browse products, add items to a shopping cart, finalize orders, and automatically update product stock.  
The system also includes features such as coupon generation and order tracking, demonstrating how a real online store backend can be structured.

## Features

- Product management (create, update, delete, list products)
- Shopping cart system
- Add and remove items from cart
- Update product quantities
- Order creation and finalization
- Automatic stock output registration
- Coupon generation after a number of purchases
- Order status management

## Technologies Used

- Python
- FastAPI
- SQLAlchemy (ORM)
- SQLite / relational database
- REST API architecture

## Project Structure

project/

├── models/ # Database models  
├── routes/ # API routes  
├── schemas/ # Data validation schemas  
├── database/ # Database configuration  
└── main.py # Application entry point  

## Installation

1. Clone the repository

git clone https://github.com/Yuri09-hub/E-commerce-system-with-shopping-cart

2. Enter the project folder

cd E-commerce-system-with-shopping-cart

3. Create virtual environment

python -m venv venv

4. Activate environment

venv\Scripts\activate

5. Install dependencies

pip install -r requirements.txt

## Running the API

uvicorn main:app --reload

API documentation will be available at:

http://127.0.0.1:8000/docs

## Business Logic

- Users can add products to a shopping cart.
- When an order is finalized, all cart items are processed and recorded as product output (stock movement).
- After a specific number of finalized orders, the user receives a discount coupon with a limited validity period.

## Author

Yuri Rodrigues   
Angola
