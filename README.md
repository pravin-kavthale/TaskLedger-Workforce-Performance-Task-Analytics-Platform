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

## 🖼️ Diagrams

### ER Diagram
![ER Diagram](Documents/ER%20diagram.png)  
*Relational schema showing PK/FK relationships across all modules.*

### Module Diagram
![Module Diagram](Documents/Module%20Diagram.png)  
*High-level module interactions between frontend, backend, and database components.*

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

## Authentication & Authorization (JWT)

The API uses **JWT (JSON Web Tokens)** for stateless authentication. Session-based auth is avoided so the backend does not store server-side session state, which simplifies horizontal scaling, works cleanly with multiple clients (web, mobile, programmatic), and avoids cookie/CSRF concerns for API-only consumers.

- **Access token:** Short-lived credential for authorizing requests. Carried in the `Authorization: Bearer <token>` header.
- **Refresh token:** Long-lived credential used only to obtain a new access token. Not sent with every request; used only against the refresh endpoint.

**Token format & strategy:** Tokens are signed with **RS256** (asymmetric: private key for signing, public key for verification). Access tokens expire in **15 minutes**; refresh tokens in **1 day**. Custom claims include `user_id`, `role`, `username`, and `email` so protected endpoints can authorize without extra DB lookups. Security considerations: tokens are opaque to the client (no sensitive data in payload beyond identifiers and role), HTTPS is required in production, and refresh tokens are rotated on use with optional blacklisting to limit reuse.

### Authentication Flow (Step-by-Step)

1. **Login request** — Client sends `POST /api/auth/login/` with `email` and `password` (JSON).
2. **Credential validation** — Backend validates against the user model (email as `USERNAME_FIELD`). Invalid credentials return 401.
3. **JWT issuance** — On success, backend returns JSON: `access` and `refresh` tokens (and optionally user payload). Access token contains standard claims plus custom claims (e.g. `role`, `user_id`).
4. **Client-side token storage** — Store the access token in memory or a short-lived, secure store for attaching to requests. Store the refresh token in **HTTP-only, Secure, SameSite cookies** (or another secure storage such as secure storage on mobile) so it is not exposed to JavaScript. Never put refresh tokens in `localStorage` if the app is exposed to XSS.
5. **Protected API requests** — Client sends `Authorization: Bearer <access_token>` on each request to protected endpoints. The backend validates the JWT signature and expiry and loads the user from the token claims.
6. **Token refresh** — When the access token expires (e.g. 401 response), client calls `POST /api/auth/refresh/` with the refresh token (in body or cookie). Backend returns a new access token (and, if rotation is enabled, a new refresh token). Old refresh token is invalidated/blacklisted after rotation.
7. **Logout & invalidation** — Client discards the access token. If refresh token rotation with blacklist is enabled, the last-used refresh token is already invalid after a refresh; for explicit logout, call a logout endpoint that blacklists the current refresh token so it cannot be reused.

### JWT Authentication Flow Diagram
![ER Diagram](Documents/JWT_Auth_Flow.png)  
### Role-Based Access Control (RBAC)

Roles (`ADMIN`, `MANAGER`, `EMPLOYEE`) are stored on the user model and **embedded in JWT claims** at login via a custom token serializer. The backend does not rely only on the token’s role claim for critical decisions: the authenticated user is loaded from the database (by `user_id` from the token), so role changes take effect after the next login or token refresh.

Permission enforcement is done with **DRF permission classes** (e.g. `IsAuthenticated`, custom `IsAdmin`, `IsAdminOrManager`) attached to views. These classes read `request.user.role` (the user instance attached by JWT authentication) and allow or deny access. Middleware is not used for role checks; all role-based authorization is view-level permission checks.

- **ADMIN** — Full access to admin-only views (e.g. user creation with any role).
- **MANAGER** — Access to manager and employee-level views (e.g. create users with EMPLOYEE role).
- **EMPLOYEE** — Access only to views that require `IsAuthenticated` or employee-specific permissions.

### Security Notes

- **Token expiration:** Short-lived access tokens (15 min) limit the window of misuse if a token is leaked. Refresh tokens (1 day) are used only at the refresh endpoint.
- **Refresh token rotation:** When rotation is enabled, each refresh returns a new refresh token and the previous one is invalidated. Optionally, the old refresh token is blacklisted so it cannot be reused. This limits damage from refresh token theft.
- **Protection against token theft:** Rely on HTTPS everywhere; store refresh tokens in HTTP-only (and Secure, SameSite) cookies where possible; avoid exposing refresh tokens to scriptable storage. Rotate and blacklist refresh tokens so a single stolen refresh token has limited use.

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
