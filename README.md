# TaskLedger – Workforce Performance & Task Analytics Platform

## 📄 Project Description

**TaskLedger** is a modular workforce management system designed to track tasks, time-based activities, and performance metrics across employees, teams, and departments.

The platform focuses on **structured task execution**, **event-driven time tracking**, and **analytics-ready data modeling**, making it suitable for enterprise environments and data-driven performance evaluation.

This repository currently contains:
- Finalized **system architecture & ER design**
- Branding and UI direction
- Planned frontend and backend module structure

Backend implementation will be developed incrementally using a clean, scalable design approach.

---

## 🎯 Core Objectives

- Centralized task and project management  
- Accurate event-based tracking of work activity  
- Role-based access for Admins, Managers, and Employees  
- Analytics-ready data for productivity insights  
- Clean separation between domain modules  

---

## 🧱 High-Level Architecture

### Frontend
- React (manual implementation planned)
- Homepage with product overview and login entry
- Dashboard UI (future scope)

### Backend
- Django + Django REST Framework (planned)
- Modular app-based architecture
- Event-driven task tracking

### Database
- Relational schema with strict PK/FK relationships
- Designed using ER principles (Eraser.io)

---

## 🗂️ Finalized Core Modules

### User & Access Control
- User  
- Role  
- UserRole  
- Profile  

### Organization Structure
- Department  
- Project  
- ProjectMember  

### Task & Activity Tracking
- Task  
- TaskEvent  
- ActivityLog  

### Analytics (Planned)
- Event-based aggregation
- Project productivity metrics
- Department and employee performance insights

---

## 🔗 Entity Relationships (Overview)

- A **User** can have multiple **Roles**
- A **User** owns exactly one **Profile**
- A **Profile** belongs to a **Department**
- A **Project** belongs to a **Department** and is managed by a **User**
- **Projects** contain multiple **Tasks**
- **Tasks** are assigned to **Users**
- **TaskEvents** track task lifecycle actions
- **ActivityLogs** capture system-level actions for auditing

---

## 🎨 Branding & UI Direction

- **Logo:** Minimal, professional, productivity-focused
- **Primary Theme:** Blue-based palette (trust, structure, analytics)
- **Homepage Design:**
  - Product introduction
  - Feature highlights
  - Login call-to-action

UI prototyping is handled using **Figma** with AI-assisted design tools.

---

## 🚧 Current Project Status

- ✔ Architecture finalized  
- ✔ ER diagram completed  
- ✔ Branding & logo finalized  
- ✔ Homepage design planned  

**Next Phase**
- Backend development (Django)
- API design & implementation
- Frontend implementation (React)

---

## ⚠️ Scope & Intent

This project is developed as a **serious portfolio / SaaS-style system**, not a tutorial or demo clone.

Features are added **only when they are properly designed, justified, and scalable**.

---

## 🛠️ Planned Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL  
- **Frontend:** React  
- **Authentication:** JWT + Role-Based Access Control  
- **Design:** Figma, AI-assisted branding tools  

---

## 📌 Roadmap (High-Level)

1. Backend core setup & authentication
2. Task & event tracking APIs
3. Analytics data modeling
4. Frontend dashboard integration
5. Performance metrics & reporting

---

## 📄 License

This project is currently under development. License will be defined once the core system stabilizes.
