# 🗳️ D-Vote – Decentralized Voting System

## 📌 Project Overview

**D-Vote** is a secure web-based voting system developed using **Python and Django** to provide a simple, transparent, and controlled digital voting process.

The system allows eligible voters to register using their **Aadhaar number, Voter ID, email, age, gender, and constituency information**. Registered voters can securely log in, view candidates belonging to their constituency, cast their vote once, and receive a voting confirmation receipt.

The system also provides **live election results before the election closes** and **final election results after voting ends**, including vote distribution, voter turnout, gender distribution, age-group analysis, and winner/tie detection.

---

## 🎯 Objectives

The main objectives of D-Vote are:

* To provide a digital alternative to manual voting.
* To verify voter eligibility before registration.
* To ensure **one voter can cast only one vote**.
* To restrict voting according to the configured election schedule.
* To display candidates according to the voter's constituency.
* To provide transparent election results.
* To calculate voter turnout and demographic statistics.
* To generate an official PDF voting confirmation receipt.
* To simplify election administration.

---

## ✨ Key Features

### 👤 Voter Registration

The voter registration system collects:

* Aadhaar Number
* Voter ID
* Email
* Age
* Gender
* Constituency
* Password

The system verifies whether the voter exists in the **pre-approved voter list** before allowing registration.

### 🔐 Voter Eligibility Verification

A voter is allowed to register only when the following information matches the pre-approved voter database:

* Aadhaar Number
* Voter ID
* Constituency

The system also verifies that the voter is **18 years or older**.

### 🔑 Secure Login

Registered voters can log in using:

* Voter ID
* Password

Django's authentication system is used to manage user authentication.

### 🗳️ One Person – One Vote

The system uses a `has_voted` flag for every registered voter.

After successfully casting a vote:

```text
has_voted = True
```

The voter cannot submit another vote.

The voting time is also recorded using:

```text
voted_at
```

### 📍 Constituency-Based Voting

Candidates are associated with specific locations/constituencies.

Current locations include:

* Doranahalli
* Shahapur
* Jayanagar
* Vasantapura
* Hosur

Voters can view candidates belonging to the selected constituency.

### 🏛️ Candidate Management

Candidates contain:

* Candidate name
* Political party
* Constituency
* Vote count
* Party logo

Supported parties in the current system include:

* BJP
* Congress
* JDS
* BSP

### ⏰ Election Time Control

The election system uses configurable:

* Voting date
* Start time
* End time

The application controls registration, login, voting, live results, and final results according to the configured election schedule.

### 📊 Live Results

Before the election closes, authorized result pages can display:

* Candidate names
* Political parties
* Vote counts
* Vote percentages
* Total votes
* Candidate comparison
* Vote-share visualization

### 🏆 Final Results

After the election ends, the system displays the final election result.

It includes:

* Winner
* Winning party
* Total votes
* Candidate-wise vote distribution
* Vote percentages
* Tie detection
* Voter turnout
* Gender distribution
* Age-group analysis

### ⚖️ Tie Detection

The system checks whether multiple candidates have received the highest number of votes.

If two or more candidates have the same maximum vote count, the system identifies the election as a **tie** instead of incorrectly declaring a single winner.

### 📈 Voter Demographics

The final results provide demographic analysis of voters who participated in the election.

The system calculates:

**Gender:**

* Male voters
* Female voters

**Age groups:**

* 18–25
* 26–40
* Above 40

### 📊 Voter Turnout

The system calculates voter turnout using:

```text
Voter Turnout =
(Number of voters who voted / Total registered voters) × 100
```

### 🧾 PDF Voting Receipt

After voting, the voter can download a **D-Vote Official Voting Receipt** in PDF format.

The receipt contains:

* Voter ID
* Aadhaar Number
* Constituency
* Voting date
* Voting status

The PDF is generated using **ReportLab**.

### 🔑 Forgot / Reset Password

Registered voters can reset their password through the forgot-password and reset-password functionality.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │        Voter         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   D-Vote Web Portal  │
                    │       Django         │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │ Registration│    │   Voting   │    │  Results   │
      └──────┬─────┘    └──────┬─────┘    └──────┬─────┘
             │                 │                 │
             ▼                 ▼                 ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │ Pre-approved│    │ Candidate  │    │ Statistics │
      │ Voter Data │    │ Vote Count │    │ & Analysis │
      └──────┬─────┘    └──────┬─────┘    └────────────┘
             │                 │
             └─────────────────┼─────────────────┐
                               ▼                 │
                    ┌──────────────────────┐     │
                    │     SQLite Database  │◄────┘
                    └──────────────────────┘
```

---

# 🔄 Voting Workflow

```text
Start
  │
  ▼
Voter Registration
  │
  ▼
Check Aadhaar + Voter ID
  │
  ▼
Check Pre-approved Voter List
  │
  ▼
Age Verification (18+)
  │
  ▼
Create Voter Account
  │
  ▼
Voter Login
  │
  ▼
Select Constituency
  │
  ▼
View Candidates
  │
  ▼
Cast Vote
  │
  ▼
Check One-Time Voting Status
  │
  ▼
Record Vote
  │
  ▼
Mark Voter as "Voted"
  │
  ▼
Generate Voting Receipt
  │
  ▼
View Election Results
```

---

# 🛠️ Technologies Used

| Technology                | Purpose                        |
| ------------------------- | ------------------------------ |
| **Python**                | Backend programming            |
| **Django 6.0.2**          | Web framework                  |
| **HTML5**                 | Web page structure             |
| **CSS3**                  | User interface styling         |
| **JavaScript**            | Dynamic frontend functionality |
| **SQLite**                | Database                       |
| **Django Authentication** | User authentication            |
| **ReportLab**             | PDF receipt generation         |
| **Chart.js**              | Result visualization           |
| **Git/GitHub**            | Version control                |

---

# 📂 Project Structure

```text
final/
│
├── mainproject/
│   │
│   ├── manage.py
│   ├── db.sqlite3
│   │
│   ├── mainproject/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── dreamgirl/
│       ├── migrations/
│       ├── templates/
│       │   └── dreamgirl/
│       │       ├── base.html
│       │       ├── home.html
│       │       ├── register.html
│       │       ├── login.html
│       │       ├── vote.html
│       │       ├── dashboard.html
│       │       ├── results.html
│       │       ├── final_results.html
│       │       ├── select_location.html
│       │       ├── forgot_password.html
│       │       ├── reset_password.html
│       │       └── result_not_declared.html
│       │
│       ├── static/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── routing.py
│       └── tests.py
│
└── README.md
```

---

# 🗃️ Database Models

The project contains four main application models.

## Candidate

Stores election candidate information.

```text
name
party
location
votes
party_logo
```

## Voter

Stores registered voter information.

```text
aadhaar_number
voter_id
has_voted
voted_at
email
location
age
gender
reset_code
```

The `has_voted` field is used to enforce the **one-person-one-vote** rule.

## PreApprovedVoter

Contains voters who are eligible to register.

```text
aadhaar_number
voter_id
location
```

This information is checked during registration.

## ElectionSettings

Stores election timing information.

```text
voting_date
start_time
end_time
```

This allows the application to control when election-related activities are available.

---

# 🔒 Security and Validation

The application implements several validation mechanisms:

* Voter authentication
* Password authentication through Django
* Pre-approved voter verification
* Aadhaar number uniqueness
* Voter ID uniqueness
* Email uniqueness
* Minimum age validation
* Voter ID format validation
* Password confirmation
* One-time vote restriction
* Election time restrictions
* Admin-controlled candidate management

### Voter ID Validation

The current application validates the Voter ID using the pattern:

```text
ABC1234567
```

That is:

```text
3 uppercase letters + 7 digits
```

---

# ⚙️ Installation and Setup

## 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

## 2. Navigate to the Project

```bash
cd final/mainproject
```

## 3. Create a Virtual Environment

```bash
python -m venv .venv
```

## 4. Activate the Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

## 5. Install Required Packages

Install Django:

```bash
pip install django
```

Install Pillow for image fields:

```bash
pip install Pillow
```

Install ReportLab for PDF generation:

```bash
pip install reportlab
```

If Chart.js is included through the frontend, no Python package is required for Chart.js.

## 6. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Create an Admin Account

```bash
python manage.py createsuperuser
```

Enter the requested username, email, and password.

## 8. Start the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 👨‍💼 Admin Workflow

The administrator can manage the election through the Django admin panel.

```text
Admin Login
     ↓
Election Settings
     ↓
Add Candidates
     ↓
Add Pre-approved Voters
     ↓
Configure Election Date & Time
     ↓
Monitor Election
     ↓
View Results
```

Candidate records are restricted from editing and deleting through the configured admin permissions.

---

# 📊 Results and Analytics

The system provides election analytics such as:

### Candidate Vote Share

```text
Candidate Votes
------------------------- × 100
Total Votes
```

### Voter Turnout

```text
Voted Voters
------------------------- × 100
Registered Voters
```

### Demographic Analysis

The final results analyze participating voters according to:

* Gender
* Age group
* Constituency

---

# 🧾 Voting Receipt

After successfully casting a vote, the voter can download:

```text
D-Vote Official Voting Receipt
```

The receipt confirms:

```text
Voter ID
Aadhaar Number
Constituency
Voting Date
Vote Successfully Cast
```

---

# 🚀 Future Enhancements

The current system can be further enhanced with:

* Blockchain-based vote storage
* Smart contracts
* OTP-based voter verification
* Email-based voting confirmation
* SMS notification
* Biometric authentication
* Aadhaar API integration
* Voter ID verification API
* End-to-end vote encryption
* Tamper-evident audit logs
* Multi-factor authentication
* Cloud deployment
* Mobile application
* Advanced election analytics
* Improved anonymity between voter identity and vote choice

---

# ⚠️ Important Note

This project is an **academic prototype** developed for educational and final-year project purposes.

It should **not be used for real governmental or public elections** without extensive security auditing, privacy protection, independent verification, cryptographic safeguards, legal compliance, and production-grade infrastructure.

---

# 👩‍💻 Project Information

**Project Name:** D-Vote – Decentralized Voting System

**Project Type:** Final Year Project

**Department:** Computer Science and Engineering

**Framework:** Django

**Language:** Python

**Database:** SQLite

---

## 📜 License

This project is developed for **academic and educational purposes**.
