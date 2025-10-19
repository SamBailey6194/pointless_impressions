# Pointless Impressions Database Tables

---

## Table of Contents

- [Pointless Impressions Database Tables](#pointless-impressions-database-tables)
  - [Table of Contents](#table-of-contents)
  - [User (CustomUser)](#user-customuser)
  - [Custom Role](#custom-role)
  - [UserProfile](#userprofile)
  - [UserAddress](#useraddress)
  - [Category](#category)
  - [Product](#product)
  - [Reviews](#reviews)
  - [Order](#order)
  - [OrderLineItem](#orderlineitem)
  - [OrderChangeRequest](#orderchangerequest)
  - [BlogPost](#blogpost)
  - [AboutPage](#aboutpage)

---

## User (CustomUser)

| Field        | Type      | PK  | Notes / Relationships                                                                 |
|-------------|-----------|-----|--------------------------------------------------------------------------------------|
| id          | Integer   | ✔   | Auto-generated primary key                                                           |
| username    | String    |     | Unique                                                                               |
| email       | Email     |     | Unique                                                                               |
| first_name  | String    |     |                                                                                      |
| last_name   | String    |     |                                                                                      |
| date_joined | DateTime  |     | Default now                                                                          |
| is_active   | Boolean   |     | Default True                                                                         |
| is_staff    | Boolean   |     | Django admin                                                                         |
| is_superuser| Boolean   |     | Django admin                                                                         |
| is_owner    | Boolean   |     | From CustomRoles                                                                     |
| is_manager  | Boolean   |     | From CustomRoles                                                                     |
| is_customer | Boolean   |     | From CustomRoles                                                                     |

**Relationships:**  
- One-to-One → UserProfile  
- One-to-Many → Orders  
- One-to-Many → OrderChangeRequests  
- Many-to-Many → CustomRole  
- One-to-Many → BlogPosts & AboutPage edits  

---

## Custom Role

| Field       | Type   | PK  | Notes / Relationships                  |
|------------|--------|-----|---------------------------------------|
| id         | Integer| ✔   | Auto-generated primary key             |
| name       | String |     | e.g., Owner, Manager, Customer        |
| description| Text   |     | Optional                              |

**Relationships:**  
- Many-to-Many → User  

---

## UserProfile

| Field              | Type        | PK  | Notes / Relationships                  |
|-------------------|------------|-----|----------------------------------------|
| id                | Integer    | ✔   | Auto-generated primary key              |
| user              | OneToOne(User)|    | 1:1 relationship                       |
| phone_number      | String     |     | Optional                               |
| default_address   | FK → UserAddress | | Optional                               |
| newsletter_opt_in | Boolean    |     | Default False                           |

**Relationships:**  
- One-to-Many → UserAddress  
- One-to-Many → Orders  

---

## UserAddress

| Field         | Type        | PK  | Notes / Relationships |
|---------------|------------|-----|----------------------|
| id            | Integer    | ✔   | Auto-generated primary key |
| user_profile  | FK → UserProfile | | 1:N relationship         |
| full_name     | String     |     |                        |
| address_line1 | String     |     |                        |
| address_line2 | String     |     | Optional               |
| city          | String     |     |                        |
| county        | String     |     | Optional               |
| postcode      | String     |     |                        |
| country       | String     |     |                        |
| is_default    | Boolean    |     | Default False          |

---

## Category

| Field        | Type   | PK  | Notes / Relationships       |
|--------------|--------|-----|-----------------------------|
| id           | Integer| ✔   | Auto-generated primary key  |
| name         | String |     | e.g., Landscape, Portrait  |
| friendly_name| String |     | Display name                |
| slug         | Slug   |     | For URLs                    |

**Relationships:**  
- One-to-Many → Product  

---

## Product

| Field       | Type        | PK  | Notes / Relationships           |
|------------|------------|-----|---------------------------------|
| id         | Integer    | ✔   | Auto-generated primary key      |
| category   | FK → Category |   | Optional                        |
| name       | String     |     |                                 |
| description| Text       |     |                                 |
| price      | Decimal    |     |                                 |
| sku        | String     |     | Optional unique SKU             |
| image      | ImageField |     |                                 |
| is_available| Boolean   |     | Default True                    |
| created_at | DateTime   |     |                                 |
| updated_at | DateTime   |     |                                 |

**Relationships:**  
- One-to-Many → OrderLineItem  
- Uploaded by User  

---

## Reviews

| Field        | Type    | Notes                          |
|-------------|---------|--------------------------------|
| id (PK)     | Integer | Primary key                    |
| product_id (FK)| Integer | References Product            |
| user_id (FK, optional)| Integer | Null if guest review     |
| rating      | Integer | Usually 1–5 stars              |
| comment     | Text    | The review content             |
| created_at  | DateTime| Timestamp                       |
| approved    | Boolean | Admin approves before showing  |

---

## Order

| Field         | Type        | PK  | Notes / Relationships                        |
|---------------|------------|-----|---------------------------------------------|
| id            | Integer    | ✔   | Auto-generated primary key                   |
| order_number  | String     |     | Unique                                      |
| user_profile  | FK → UserProfile | | Optional (guest checkout)                 |
| full_name     | String     |     |                                             |
| email         | Email      |     |                                             |
| phone_number  | String     |     |                                             |
| address_line1 | String     |     |                                             |
| address_line2 | String     |     | Optional                                    |
| city          | String     |     |                                             |
| postcode      | String     |     |                                             |
| country       | String     |     |                                             |
| date          | DateTime   |     | Auto now                                    |
| delivery_cost | Decimal    |     | Default 0                                   |
| order_total   | Decimal    |     |                                             |
| grand_total   | Decimal    |     |                                             |
| stripe_pid    | String     |     | Payment ID                                  |
| original_bag  | Text       |     | JSON of cart data                           |
| order_status  | String     |     | Enum (“Pending”, “Paid”, “Dispatched”)     |
| tracking_token| UUID       |     | Unique link for guest tracking             |

**Relationships:**  
- One-to-Many → OrderLineItem  
- One-to-Many → OrderChangeRequest  

---

## OrderLineItem

| Field       | Type    | PK  | Notes / Relationships   |
|------------|--------|-----|------------------------|
| id         | Integer| ✔   | Auto-generated primary key |
| order      | FK → Order |  | 1:N                    |
| product    | FK → Product | | 1:N                    |
| quantity   | Integer |     | Default 1              |
| lineitem_total | Decimal | | price × quantity       |

---

## OrderChangeRequest

| Field       | Type    | PK  | Notes / Relationships         |
|------------|--------|-----|-------------------------------|
| id         | Integer| ✔   | Auto-generated primary key     |
| order      | FK → Order | | 1:N                            |
| user       | FK → User  | | Request submitted by user     |
| request_type | String  |     | Enum (“Cancel”, “Change Address”) |
| message    | Text    |     | Optional                       |
| status     | String  |     | Enum (“Pending”, “Approved”, “Denied”) |
| created_at | DateTime|     | Auto now                        |

---

## BlogPost

| Field       | Type      | PK  | Notes / Relationships         |
|------------|----------|-----|-------------------------------|
| id         | Integer  | ✔   | Auto-generated primary key     |
| title      | String   |     |                               |
| slug       | Slug     |     | Unique                        |
| content    | RichText |     |                               |
| image      | ImageField |   | Optional                       |
| author     | FK → User |     | Owner/Manager only             |
| created_at | DateTime |     |                               |
| updated_at | DateTime |     |                               |
| is_published | Boolean |   | Default False                  |

---

## AboutPage

| Field       | Type      | PK  | Notes / Relationships         |
|------------|----------|-----|-------------------------------|
| id         | Integer  | ✔   | Auto-generated primary key     |
| title      | String   |     |                               |
| content    | RichText |     | Editable by admin             |
| image      | ImageField |   | Optional                       |
| updated_at | DateTime |     | Auto now                       |
| updated_by | FK → User |     | Owner/Manager only             |
