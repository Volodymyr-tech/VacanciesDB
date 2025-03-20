# HeadHunter Vacancies with PostgreSQL Integration

This project is a tool for working with job vacancies collected from the HeadHunter website, with the ability to save data either to a PostgreSQL database or a JSON file. It is useful for analyzing vacancies and employers.

## Features

### 1. HeadHunter API
- **Classes:**
  - `HH` ([class_api.py](./class_api.py)): Handles interaction with the HeadHunter API, fetching job listings by keyword and retrieving employer information.
  - `EmpHH` ([class_api_employers.py](./class_api_employers.py)): Alternative class for working with the API, includes logging.

- **Methods:**
  - Load vacancies by keyword.
  - Retrieve employer information.
  - Load vacancies related to specific employers.

---

### 2. Data Storage
- **Class:** `JsonSaver` ([class_json_saver.py](./class_json_saver.py))
  - Saves vacancies to a JSON file.
  - Supports adding, deleting, and filtering vacancies.
  - Sorts vacancies by salary.

- **Class:** `DBManager` ([class_db_manager.py](./class_db_manager.py))
  - Saves vacancy and employer data to PostgreSQL.
  - Provides methods to:
    - Get a list of companies with vacancy counts.
    - Retrieve all vacancies with employer and salary info.
    - Calculate average salary.
    - Get vacancies with salaries above the average.
    - Search vacancies by keyword.

---

### 3. Database Management
- **Class:** `CreateDb` ([class_create_db.py](./class_create_db.py))
  - Creates the database and tables `employers` and `vacancies`.

- **Class:** `DbConn` ([class_connection_to_db.py](./class_connection_to_db.py))
  - Manages PostgreSQL connections using environment variables.

---

### 4. User Interaction
- **Class:** `UserInteraction` ([user_interaction.py](./user_interaction.py))
  - Interacts with JSON data:
    - Search vacancies by keyword.
    - Sort and filter vacancies.
    - Delete vacancies by URL.

- **Class:** `InteractionPostgre` ([user_interaction_postgres.py](./user_interaction_postgres.py))
  - Interacts with PostgreSQL:
    - Create database and tables.
    - Save data from API.
    - Query, sort, and filter vacancies.

---

## Installation and Setup

### Requirements
- Python 3.9+
- PostgreSQL
- Dependencies managed with **Poetry**

### Installation
1. Clone the repository:
   git clone <URL>
   cd <REPO_NAME>

## Install dependencies:
poetry install
