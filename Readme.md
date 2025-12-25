# TechieBright – Frontend (Angular)

TechieBright is an AI-driven career intelligence platform for the IT industry that combines curated global skill data with real-world job insights to help individuals and organizations understand what skills matter, which roles they align with, and how to prepare effectively.

The platform allows users to create employee profiles, explore global skill–role mappings, receive structured AI recommendations grounded in industry datasets, and track learning roadmaps over time — enabling informed career growth and hiring readiness.

This repository contains the **Angular frontend** of the TechieBright platform.

---

## ✨ Features

- Employee profile creation and management
- Global skills & job roles dashboard
- Skill → Role intelligence mapping
- AI recommendation interface
- AI recommendation history (edit / delete)
- Responsive, dashboard-style UI
- Clean card-based layout for all major pages

---

## 🧠 Core Pages

- **Employees**
  - Create and manage employee profiles
  - Navigate to individual employee dashboards

- **Employee Dashboard**
  - View employee details and skills
  - Entry point for AI recommendations and analysis

- **Global Skills & Roles Intelligence**
  - Explore IT skills and job roles
  - Understand how skills map to real-world roles

- **AI Recommendation**
  - Ask career or skill-related questions
  - Receive structured AI guidance

- **AI Recommendation History**
  - View, edit, and delete past AI recommendations

---

## 🛠 Tech Stack

- Angular (Standalone Components)
- TypeScript
- SCSS (custom design system)
- RxJS
- Angular Router
- REST API integration (Django backend)

---

## 📂 Project Structure

src/
├── app/
│ ├── core/ # API services
│ ├── features/ # Feature modules (employees, dashboard, history, etc.)
│ ├── models/ # TypeScript models
│ └── app.routes.ts # Application routes
└── styles.scss


---

## 🚀 Getting Started

### 1️⃣ Install dependencies
npm install

 ### 2️⃣ Run the development server
ng serve

### 3️⃣ Open in browser
http://localhost:4200




🔗 Backend Dependency

This frontend requires the TechieBright Django backend to be running.

Make sure:

Backend runs on http://localhost:8000

CORS is enabled

API endpoints are accessible

🎨 UI Design Philosophy

Card-based dashboard layout

Consistent headers and spacing

Responsive-first design

Clear separation of concerns

Focus on clarity over clutter

📌 Future Enhancements

Skill gap analysis visualization

Demand badges (High / Medium / Low)

Charts and analytics

Authentication & user accounts

Improved accessibility

🤝 Contributing

Contributions are welcome!

Fork the repo

Create a feature branch

Submit a pull request

📄 License

This project is open-source.


---

# 📘 `README.md` — **Backend (Django)**

# TechieBright – Backend (Django)


This repository contains the **Django backend** for TechieBright.

---

## ✨ Features

- Employee profile management
- Global skills & roles knowledge base
- Skill → role mapping engine
- AI-powered career recommendations
- AI recommendation history (CRUD)
- Dataset-driven market insights
- RESTful APIs for frontend integration

---

## 🧠 Key Concepts

- **Global Data**  
  Curated skills and roles act as a controlled vocabulary to prevent AI hallucination.

- **Dataset Enrichment**  
  Kaggle datasets are processed offline and cached as JSON for fast access.

- **AI Guardrails**  
  AI responses are constrained to known skills and roles.

---

## 🛠 Tech Stack

- Python
- Django
- MySQL
- Groq API (LLM inference)
- JSON-based dataset caching
- Django ORM

---

## 📂 Project Structure



core/
├── models.py # Database models
├── views/
│ ├── ai.py # AI recommendation endpoints
│ ├── employees.py # Employee APIs
│ └── global_data.py # Global skills & roles APIs
├── services/
│ ├── global_data_service.py
│ └── dataset_cache.py
├── datasets/ # Kaggle & processed datasets


---

## 🚀 Getting Started

### 1️⃣ Create virtual environment


python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Configure environment variables

Create a .env file:

GROQ_API_KEY=your_api_key_here

4️⃣ Run migrations
python manage.py migrate

5️⃣ Start the server
python manage.py runserver


Server will run at:

http://localhost:8000

🔌 Core API Endpoints
Employees

GET /api/employees/

POST /api/employees/add/

GET /api/employees/<id>/

PUT /api/employees/by-user/<id>/update-skills/

Global Data

GET /api/global/skills/

GET /api/global/roles/

GET /api/global/skill-role-map/

AI Recommendations

POST /api/ai/recommend/

GET /api/ai/history/<user_id>/

PUT /api/ai/history/edit/<id>/

DELETE /api/ai/history/delete/<id>/

🧠 Dataset Integration

Kaggle datasets are processed using Python scripts

Raw CSV files are converted into normalized JSON

Cached in memory via dataset_cache.py

Ensures fast lookups and consistent AI enrichment

🔒 AI Safety & Design

AI responses are forced into strict JSON

Skills and roles are selected only from known global lists

Dataset insights are injected post-AI response

Prevents hallucination and ensures explainability

📌 Future Enhancements

Authentication & user accounts

Admin panel for dataset updates

Skill demand trend analysis

Recommendation scoring

Employer-focused analytics

🤝 Contributing

Contributions are welcome!

Fork the repository

Create a feature branch

Submit a pull request

📄 License

This project is open-source and available under the MIT License.


---
