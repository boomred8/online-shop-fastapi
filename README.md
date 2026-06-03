# 🛒 Online Shop (FastAPI + PostgreSQL)

Простой интернет-магазин с каталогом товаров, корзиной и системой оформления заказов.

---

# 🚀 Описание проекта

Проект представляет собой веб-приложение интернет-магазина, разработанное с использованием FastAPI и серверного рендеринга через Jinja2.

Пользователь может:

- просматривать каталог товаров
- открывать карточки товаров
- добавлять товары в корзину
- изменять количество товаров
- удалять товары из корзины
- оформлять заказы
- просматривать историю заказов

Для товаров реализована система доступности `Out of Stock`.

---

# 🧠 Технологии

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Jinja2
- Docker
- Docker Compose
- Uvicorn

---

# ⚙️ Как работает

1. Пользователь открывает каталог товаров
2. Выбирает товар
3. Добавляет товар в корзину
4. Изменяет количество товаров при необходимости
5. Переходит к оформлению заказа
6. Указывает имя и номер телефона
7. Заказ сохраняется в базе данных PostgreSQL
8. Заказ отображается в разделе истории заказов

---

# 📁 Структура проекта

```text
ProjectTask/
│
├── app/
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── product.py
│   │   ├── order.py
│   │   └── order_item.py
│   │
│   ├── routers/
│   │   ├── products.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   └── pages.py
│   │
│   ├── schemas/
│   │   ├── product.py
│   │   └── order.py
│   │
│   └── main.py
│
├── templates/
│
├── static/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

#🗄️ База данных
## 🗄️ Database Schema

```text
Product
├── id
├── name
├── description
├── price
├── image
└── is_available

Order
├── id
├── customer_name
├── phone_number
└── created_at

OrderItem
├── id
├── order_id
├── product_id
└── quantity
```

--- 
## 🛍️ Features

### 📦 Product Catalog
- View all products
- View product details
- Display product image
- Display product price
- Display product description

### 🛒 Shopping Cart
- Add product to cart
- Remove product from cart
- Increase quantity
- Decrease quantity
- Calculate total price

### 📋 Order Management
- Enter customer name
- Enter phone number
- Save order to PostgreSQL database

### 📦 Product Availability
- Display product availability status
- Show **Out of Stock** status
- Prevent adding unavailable products to cart

## 🐳 Run with Docker

### Build and start the project

```bash
docker compose up --build
```

After startup, the application will be available at:

```text
http://localhost:8000
```

### Swagger Documentation

```text
http://localhost:8000/docs
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
PG_DATABASE=postgresql+asyncpg://postgres:postgres@db:5432/shop_db
```

---

## 🧪 Main Use Cases

- View product catalog
- View product details
- Add products to cart
- Update product quantity in cart
- Remove products from cart
- Create orders
- View order history
- Change product availability status

---

## 🧠 Features

- Asynchronous PostgreSQL integration
- Server-side rendering with Jinja2
- Simple FastAPI architecture
- Docker Compose for quick deployment
- Swagger API documentation
- Scalable project structure

---

## 👨‍💻 Author

**Ali Kabiyev**

- Telegram: @kabiev69
- GitHub: https://github.com/boomred8