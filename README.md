# Project Setup and Running Instructions

## Cloning the Repository

First, clone the repository using the following command:

```bash
git clone https://github.com/chaitanya1347/pdf_sql_chatbot.git
```

## Frontend Setup

Navigate to the frontend directory:
```bash
cd frontend
```

Install the necessary dependencies::
```bash
npm install
```

Start the frontend application:
```bash
npm run start
```

## Backend Setup

### Update GOOGLE and AWS API Key in .env file

open new terminal 
Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment:
```bash
python -m venv myenv
```

Activate the virtual environment:
On Windows:
```bash
.\myenv\Scripts\activate
```
On macOS/Linux:
```bash
source myenv/bin/activate
```

Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

Run the backend application:
```bash
python main.py
```
