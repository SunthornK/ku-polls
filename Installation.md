## Installation Guide for KU Polls

This guide will help you install and configure the KU Polls application on your local machine.

## 1. Clone the Repository
To get started, clone the repository from GitHub:

```bash
git clone https://github.com/SunthornK/ku-polls.git
cd ku-polls
```

## 2. Set Up a Virtual Environment
Set up a Python virtual environment in your project folder and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## 3. Install Dependencies
Install all the dependencies listed in requirements.txt:
```bash
pip install -r requirements.txt
```

## 4. Set Values for Externalized Variables
In the project root directory, you'll find a `sample.env` file. Copy this file and rename it to `.env`:
```bash
cp sample.env .env
```

## 5. Run Migrations
Apply the database migrations to set up the necessary tables:
```bash
python manage.py migrate
```
## 6. Run Tests
To ensure everything is set up correctly, run the project's test suite:
```bash
python manage.py test
```
## 7. Install Data from Fixtures
To load demo data (such as users and poll questions), use the following command:
1. Questions and Choices (No Votes):
   ```bash
   #This will load poll questions and their choices
   python manage.py loaddata data/polls-v4.json
   
2. Votes: 
   ```bash
   #This will load the vote data
   python manage.py loaddata data/polls-v4.json
   
3. Users: 
   ```bash
   #This will load the user accounts
   python manage.py loaddata data/users.json
