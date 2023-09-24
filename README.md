# FastAPI-ecommerce

### API Live on - https://fastapi-ecommerce.onrender.com/
### API Docs - https://fastapi-ecommerce.onrender.com/docs

### And if you like this project, then ADD a STAR ⭐️  to this project 👆

## How to Install and Run this project?

### Pre-Requisites:
1. Install Git Version Control
[ https://git-scm.com/ ]

2. Install Python Latest Version
[ https://www.python.org/downloads/ ]
#### Use python 3.11.4 or above

3. Install Pip (Package Manager)
[ https://pip.pypa.io/en/stable/installing/ ]

### Installation
**1. Navigate to directory where you want to save the project**

**2. Create a Virtual Environment and Activate**

Create Virtual Environment

For Windows
```
python -m venv env
```
For Linux
```
python3 -m venv env
```

Activate Virtual Environment

For Windows
```
env\scripts\activate
```
For Linux
```
source env/bin/activate
```

**3. Clone this project**
```
git clone https://github.com/Minal-singh/FastAPI-ecommerce.git
```

Then, Enter the project
```
cd FastAPI-ecommerce
```
**4. Install Requirements from 'requirements.txt'**
```
pip install -r requirements.txt
```
**5. Create .env file from .env.example**

Add MongoDB Atlas URI and Database name to .env

**6. Start the server**
```
uvicorn main:app --reload
```
