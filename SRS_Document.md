# Software Requirements Specification (SRS)
## Project Name: Online Token Generator (Gujarat Government)

### 1. Introduction
#### 1.1 Purpose
The purpose of this document is to define the Software Requirements Specification (SRS) for the **Online Token Generator**, a web-based application designed to streamline the process of booking appointments and generating service tokens for various government and public offices (RTO, Urban, and Rural).

#### 1.2 Scope
The system allows citizens to book tokens online, avoiding long physical queues. It caters to multiple roles including Citizens (Customers), Employees, Office Admins, and Super Admins. The system handles geographic categorizations (Districts, Talukas, Villages) and dynamically assigns token numbers based on office sequences and RTO codes. Wait times and token statuses are tracked in real-time.

### 2. Overall Description
#### 2.1 Product Perspective
The system consists of a dynamic React-based frontend frontend and a robust Django-based backend. It operates over the internet and provides responsive dashboards for different user roles. It also integrates email notifications (OTP verification) and potential blockchain-based token proofs.

#### 2.2 User Classes and Characteristics
*   **Citizen / Customer:** General public users who register, log in, find offices, and book tokens for specific services.
*   **Employee:** Office staff who serve the tokens, manage the token queue, update token statuses, and can manually generate tokens for walk-in citizens.
*   **Office Admin:** Administrators restricted to a specific office who manage employees, services, and view office-level reports.
*   **Super Admin:** System-wide administrators who manage geographical data, set up new offices, and overlook the entire system's operations.

#### 2.3 Operating Environment
*   **Frontend:** ReactJS (Responsive web application).
*   **Backend:** Python Django framework, REST APIs.
*   **Database:** PostgreSQL/SQLite (as configured in Django).
*   **Deployment:** Cloud-hosted web server accessible via modern web browsers (Chrome, Firefox, Safari, Edge).

### 3. System Features
#### 3.1 User Authentication and Authorization
*   **Description:** Secure registration and login mechanism.
*   **Functional Requirements:**
    *   Citizens must register with their Name, Email, and Mobile Number.
    *   OTP verification via email for account recovery and secure actions.
    *   Role-based access control (RBAC) redirecting users to their respective dashboards upon login.

#### 3.2 Token Booking System
*   **Description:** Core functionality for citizens to book tokens.
*   **Functional Requirements:**
    *   Users can search for offices based on District, Taluka, Village, and Office Type (Urban, Rural, RTO).
    *   Users can select a specific service to book a token.
    *   The system generates a unique alphanumeric Token Number (e.g., GJ01A001) ensuring no overlaps.
    *   Provides an estimated waiting time and a printable/downloadable Token Receipt.

#### 3.3 Token Queue Management
*   **Description:** Interface for employees to manage the daily tokens.
*   **Functional Requirements:**
    *   Employees can view the queue of tokens for their assigned office.
    *   Employees can update token status: `WAITING`, `SERVING`, `COMPLETED`, `CANCELLED`.
    *   Real-time status updates reflected on the citizen's Token Status page.

#### 3.4 Office and Geography Management
*   **Description:** Administrative module for structural setup.
*   **Functional Requirements:**
    *   Super Admins can add/edit Districts, Talukas, and Villages.
    *   Super Admins can register new Offices and assign RTO/Sequence codes.
    *   Office Admins can manage services offered and average processing times.

### 4. Non-Functional Requirements
#### 4.1 Performance Requirements
*   The system must generate a token securely within 2 seconds.
*   Dashboards should load in under 3 seconds on standard broadbands.

#### 4.2 Security Requirements
*   Passwords must be hashed securely.
*   APIs must be protected using token-based authentication (JWT).
*   Prevention of race conditions during concurrent token generation using atomic database transactions.

#### 4.3 Usability Requirements
*   The system must have a fully responsive user interface functioning seamlessly on mobile, tablet, and desktop views.
*   Interactive and intuitive UI based on a "futuristic tech-lab" or "modern government" design aesthetic.

### 5. Future Enhancements
*   SMS Notification integration.
*   Advanced Blockchain Verification for Token authenticity.
*   Live Multi-lingual localization Support.
