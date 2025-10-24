Social Media API
# 🧠 Social Media API — Django REST Framework

A backend capstone project built with **Django** and **Django REST Framework (DRF)**.  
This API simulates a real-world social media platform where users can **create posts**, **follow others**, and **view a personalized feed**.  
It demonstrates backend engineering fundamentals — user authentication, database relationships, CRUD operations, and RESTful API design.

---

## 🚀 Project Overview
As a backend developer, the goal is to **design and implement a Social Media API** capable of handling user interactions and data at scale.  

This project manages:
- User accounts and profiles  
- Post creation, retrieval, updates, and deletion  
- Following and unfollowing other users  
- Generating a feed of posts from followed users  

It mirrors real-world backend challenges such as data modeling, user relationships, API security, pagination, and deployment.

---

## 🧩 Core Features

### 📝 Post Management (CRUD)
- Create, read, update, and delete posts.
- Each post includes:
  - `content` (text)
  - `author` (user)
  - `timestamp`
  - optional `media` (image URLs)
- Validation for required fields.
- Users can only modify their own posts.

---

### 👤 User Management
- Full CRUD operations for users.
- Each user has:
  - unique `username`, `email`, and `password`
  - optional profile fields (`bio`, `profile picture`)
- Only authenticated users can create, update, or delete posts.
- Token-based authentication (JWT) supported.

---

### 🔁 Follow System
- Users can **follow** and **unfollow** others.
- Relationships stored in a dedicated `Follow` model.
- Self-following is restricted.
- Enables personalized feeds of followed users’ posts.

---

### 📰 Feed of Posts
- Displays posts from followed users.
- Supports:
  - Filtering by date range
  - Searching posts by keyword
  - Pagination and sorting by popularity or recency

---

## ⚙️ Technical Stack

| Layer | Technology |
|--------|-------------|
| **Framework** | Django 5.x, Django REST Framework |
| **Database** | MySQL |
| **Authentication** | Django Auth / JWT (via djangorestframework-simplejwt) |
| **Deployment** | PythonAnywhere |
| **Environment Management** | `pipenv` or `virtualenv` |
| **API Docs** | DRF Browsable API |

---

## 🗄️ Database Design
Main entities:
- **User** — authentication and identity
- **Profile** — one-to-one user details
- **Post** — content created by users
- **Follow** — follower/following relationship
- **Like** *(optional)* — reactions to posts
- **Comment** *(optional)* — user interactions
- **Notification** *(stretch)* — activity alerts
- **Message** *(stretch)* — direct messaging between users

All relationships and constraints follow Django ORM conventions with appropriate foreign keys, indexes, and cascade rules.

---

## 🔑 Authentication & Authorization
- Authentication: Django built-in users + JWT tokens  
- Authorization:  
  - Only authenticated users can post, follow, like, or comment.  
  - Users can only edit or delete their own posts.  
  - Public access for viewing posts and profiles.  

---

## 📡 API Design
All endpoints follow RESTful standards using appropriate HTTP methods:

| Action | HTTP Method | Endpoint |
|--------|--------------|----------|
| Register user | `POST` | `/api/register/` |
| Login (JWT) | `POST` | `/api/login/` |
| CRUD Posts | `GET, POST, PUT, DELETE` | `/api/posts/` |
| Follow / Unfollow | `POST` | `/api/follow/<user_id>/` |
| Feed | `GET` | `/api/feed/` |
| Comments | `POST, GET, DELETE` | `/api/posts/<id>/comments/` |

---

## 🧮 Pagination & Sorting
- Feed and posts are paginated (configurable in `settings.py`).
- Sortable by:
  - Date created
  - Popularity (likes or comments)

---

## 🚢 Deployment
- Environment variables managed via `.env`  
- Deployed on **PythonAnywhere**