# Smart Production Plating Scheduler

## 📌 Overview

**Smart Production Plating Scheduler** is a desktop application designed to automate production scheduling for plating operations.

The application processes production planning data provided through Excel files and generates an optimized production schedule using a priority-based scheduling approach.

The system combines a **React.js and Electron frontend** with a **Python and FastAPI backend** to provide an integrated desktop scheduling solution.

---

## 🎯 Problem Statement

Production scheduling in plating operations can involve multiple parts, machines, priorities, quantities, and processing requirements.

Manual scheduling can be:

* Time-consuming
* Difficult to manage for large production datasets
* Prone to scheduling conflicts
* Difficult to optimize for machine utilization
* Repetitive when production data changes

The Smart Production Plating Scheduler was developed to reduce manual scheduling effort and provide a structured approach to production planning.

---

## 💡 Proposed Solution

The application allows production data to be uploaded through an Excel file.

The system then:

1. Reads the production data.
2. Processes the input information.
3. Applies priority-based scheduling logic.
4. Generates a production schedule.
5. Displays the generated schedule through the desktop application.
6. Allows the generated schedule to be exported as a CSV file.

```text
Excel Production Data
        ↓
   Data Processing
        ↓
Priority-Based Scheduling
        ↓
 Schedule Generation
        ↓
 Schedule Preview
        ↓
     CSV Export
```

---

## ⭐ Key Features

### 📊 Excel-Based Input

Production planning information can be provided through Excel datasets.

The system processes the uploaded production data and uses it as the input for schedule generation.

---

### ⚙️ Priority-Based Scheduling

The application uses a priority-based scheduling approach to determine the order in which production tasks should be processed.

This helps organize production activities according to their assigned priorities and operational requirements.

---

### 🖥️ Desktop Application

The application is packaged as a desktop solution using **Electron**.

The Electron frontend provides an interactive interface for:

* Uploading production data
* Starting schedule generation
* Previewing schedules
* Exporting generated results

---

### 🔌 FastAPI Backend

A **FastAPI-based Python backend** handles the scheduling and data-processing operations.

The frontend communicates with the backend through REST APIs.

```text
React.js / Electron
        ↓
     REST API
        ↓
     FastAPI
        ↓
Python Scheduling Logic
        ↓
Generated Schedule
```

---

### 📥 Excel Upload

Users can upload production planning data through the application.

The uploaded data is processed by the backend before scheduling.

---

### 📋 Schedule Preview

After processing the production data, the generated schedule can be previewed through the application interface.

---

### 📤 CSV Export

The generated production schedule can be exported as a CSV file for further analysis, sharing, or production planning.

---

## 🏗️ System Architecture

```text
                     Smart Production
                     Plating Scheduler
                            │
                            ▼
                  React.js + Electron
                       Frontend
                            │
                            │ REST API
                            ▼
                       FastAPI
                       Backend
                            │
                            ▼
                  Python Scheduling
                       Logic
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
        Excel Input Data          Schedule Generation
                                        │
                                        ▼
                                 Schedule Preview
                                        │
                                        ▼
                                   CSV Export
```

---

## 🛠️ Technologies Used

### Frontend

* React.js
* Electron
* JavaScript
* HTML
* CSS

### Backend

* Python
* FastAPI
* REST APIs

### Data Processing

* Excel-based production datasets
* CSV output

### Development Tools

* Git
* GitHub
* Visual Studio Code
* Postman

---

## 📂 Project Structure

```text
Smart-Production-Plating-Scheduler/
│
├── backend/
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── ...
│   └── ...
│
├── frontend/
│   ├── ...
│   └── ...
│
├── .gitignore
│
└── README.md
```

> The exact files and folders may vary depending on the current implementation.

---

## ⚙️ Application Workflow

```text
Start Application
       ↓
Upload Excel Production Data
       ↓
Read Production Information
       ↓
Process Input Data
       ↓
Apply Priority Rules
       ↓
Generate Production Schedule
       ↓
Display Schedule
       ↓
Export Schedule as CSV
```

---

## 📊 Scheduling Process

The scheduling process uses production information from the uploaded dataset.

The general workflow is:

### 1. Input

Production information is provided through an Excel file.

### 2. Data Processing

The backend reads and processes the production dataset.

### 3. Priority Evaluation

Production tasks are evaluated based on their scheduling priorities.

### 4. Schedule Generation

The scheduling logic creates an ordered production schedule.

### 5. Schedule Preview

The generated schedule is displayed in the application.

### 6. Export

The final schedule can be exported as a CSV file.

---

## 🔄 Frontend–Backend Communication

The application uses a modular frontend and backend architecture.

```text
User
 │
 ▼
Electron Desktop Interface
 │
 ▼
React.js Frontend
 │
 │ HTTP / REST API
 ▼
FastAPI Backend
 │
 ▼
Python Scheduling Logic
 │
 ▼
Schedule Result
 │
 ▼
React.js Interface
```

This separation makes the scheduling logic easier to maintain and allows the frontend and backend components to be developed independently.

---

## 📈 Benefits

### Reduced Manual Scheduling

Automates repetitive scheduling activities that would otherwise require manual planning.

### Faster Production Planning

Production schedules can be generated from uploaded Excel data without manually creating the schedule.

### Priority-Based Planning

Production tasks can be organized according to predefined scheduling priorities.

### Improved Resource Utilization

The scheduling approach helps organize production tasks with the goal of improving resource utilization.

### Easy Data Export

Generated schedules can be exported as CSV files for further use.

---

## 📸 Screenshots

Screenshots and visual assets can be added to demonstrate the application.

Recommended screenshots include:

```text
screenshots/
├── application-interface.png
├── excel-upload.png
├── schedule-preview.png
└── csv-output.png
```

Example:

```markdown
![Schedule Preview](screenshots/schedule-preview.png)
```

---

## 🚀 Getting Started

### Prerequisites

The development environment requires the relevant dependencies for:

* Python
* Node.js
* npm

---

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jeevi2006/Smart-Production-Plating-Scheduler.git
```

Move into the project directory:

```bash
cd Smart-Production-Plating-Scheduler
```

---

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Install the required Python dependencies according to the project's dependency configuration.

Start the FastAPI backend using the project's configured startup command.

---

### 3. Frontend Setup

Navigate to the frontend directory and install the required Node.js dependencies:

```bash
npm install
```

Start the frontend using the project's configured development command.

---

## 🧪 Testing

The application can be tested using sample production datasets.

Testing can include:

* Excel file upload
* Input data processing
* Priority-based schedule generation
* Schedule preview
* CSV export
* Frontend-backend communication

---

## 🔐 Hardware-Based Licensing

The desktop application includes a hardware-based licensing mechanism for controlled application usage.

The licensing workflow is designed to validate the authorized hardware environment before allowing application use.

The licensing mechanism includes:

* Hardware identification
* License validation
* License expiry validation
* Protected license information

Sensitive licensing files, keys, and credentials should not be exposed in a public repository.

---

## 🧩 Project Architecture

The project separates the major components into:

### Frontend

Responsible for the desktop user interface and user interactions.

### Backend

Responsible for API handling, data processing, and scheduling operations.

### Scheduling Logic

Responsible for applying production scheduling priorities and generating the schedule.

### Data Input/Output

Responsible for processing Excel input data and generating CSV output.

---

## 🔮 Future Enhancements

Potential future improvements include:

* Advanced scheduling optimization
* Real-time production monitoring
* Machine availability integration
* Automatic scheduling based on machine capacity
* Production analytics dashboard
* Schedule comparison and optimization
* Additional scheduling constraints
* Improved visualization of production timelines
* Automated reporting

---

## 🎓 Learning Outcomes

This project provided practical experience in:

* Desktop application development
* React.js
* Electron
* Python
* FastAPI
* REST API development
* Excel data processing
* Scheduling algorithms
* Frontend-backend integration
* CSV generation
* Software architecture
* Git and GitHub

---

## 👩‍💻 Project Information

**Project Name:** Smart Production Plating Scheduler

**Domain:** Production Planning & Scheduling

**Application Type:** Desktop Application

**Frontend:** React.js, Electron

**Backend:** Python, FastAPI

**Input:** Excel Production Dataset

**Output:** CSV Production Schedule

---

## 📌 Important Note

This project is developed as a production scheduling application for educational and demonstration purposes.

The repository should not contain confidential production data, private credentials, license keys, API keys, or other sensitive information.

---

## 📄 Disclaimer

This project demonstrates the use of software development, scheduling logic, data processing, and desktop application technologies to automate production planning workflows.
