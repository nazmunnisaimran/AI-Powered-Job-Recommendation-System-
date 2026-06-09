# AI-Powered-Job-Recommendation-System-
An intelligent web application that analyzes user resumes, extracts technical skills using NLP-based parsing, and recommends relevant job opportunities. Built with Flask, SQLAlchemy, SQLite/MySQL, and PDF processing, the platform helps students and job seekers discover career opportunities aligned with their skills.
# AI-Powered Job Recommendation System

## 📌 Overview

The AI-Powered Job Recommendation System is a Flask-based web application that helps job seekers discover relevant career opportunities by analyzing their resumes.

Users can upload PDF resumes, and the system automatically extracts technical skills using NLP and pattern matching techniques. Based on the extracted skills, the recommendation engine suggests suitable job roles and learning resources to improve employability.

---

## 🚀 Features

### 👤 User Authentication
- User Registration
- Secure Login & Logout
- Password Hashing using Werkzeug
- Session Management

### 📄 Resume Upload & Parsing
- Upload resumes in PDF format
- Automatic text extraction from resumes
- Skill identification from extracted content
- Supports multiple technical skill categories

### 🧠 Skill Extraction Engine
Extracts skills from:
- Programming Languages
- Web Development Technologies
- Databases
- Cloud Platforms
- DevOps Tools
- Machine Learning & Data Science Tools

Examples:
- Python
- Java
- SQL
- React
- Flask
- AWS
- Docker
- TensorFlow
- Power BI
- Git

### 💼 Job Recommendation System
- Generates job recommendations based on extracted skills
- Matches user profiles with job requirements
- Personalized career suggestions

### 📚 Learning Resources
- Suggests learning resources for missing or required skills
- Supports continuous upskilling

### ⚡ Skill Management API
- Update skills manually
- Dynamic skill modification through frontend dashboard

---

## 🏗️ System Architecture

```text
User
 │
 ▼
Resume Upload
 │
 ▼
PDF Parser
 │
 ▼
Skill Extraction Engine
 │
 ▼
User Profile Database
 │
 ▼
Recommendation Engine
 │
 ▼
Job Recommendations
