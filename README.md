🩺 Medicine Expiry & Stock Alert System (MESAS)

A Python-based inventory management system designed to track medicine stock levels, monitor expiry dates, and generate automated alerts for pharmacies, healthcare providers, and medical distributors.
📌 Project Overview

The Medicine Expiry & Stock Alert System helps avoid:

Selling expired medicines

Running out of critical stock

Manual checking errors

The system ensures accuracy, automation, and ease of use with simple command-line interaction.

🚀 Features
🔐 1. Authentication Module

User login and signup

Admin role with higher privileges

Secure in-memory credential storage

💊 2. Medicine Management (CRUD)

Add new medicines

Update stock, expiry date, and price

Remove medicines

Search by ID or Name

Display inventory (sorted / unsorted)

⏰ 3. Alert Module

Expiry alerts for medicines expiring soon

Low-stock warnings (< 5 units)

Priority Queue ensures highest priority alerts appear first

📊 4. Report Generation

Total stock value

Number of expired medicines

Total varieties of medicines

📦 5. Data Structures Used
Functionality	Data Structure
Search by ID	Hash Table (Dictionary)
Sorted listing / Search by Name	Binary Search Tree (BST)
Alerts	Priority Queue (heapq)
Storage	List (dynamic array)
🧠 System Architecture (3-Tier Design)
1️⃣ Presentation Layer

Input prompts & display outputs

Handles menu-based interactions

2️⃣ Business Logic Layer

Authentication logic

CRUD operations

Alert generation

Report processing

3️⃣ Data Layer

Medicines list

Hash table for O(1) lookups

BST for sorted orders

Priority queue for alerts
