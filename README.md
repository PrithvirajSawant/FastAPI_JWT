# myeNovation Attendance System 

## 1: Install all the required dependencies using the following command : 
```bash
pip install -r requirements.txt
```

## 2: Create a .evn file in the root directory of the project :
```bash
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1
DataBase_URL = "mysql://user_name:password@localhost:3306/db_name"

SKIP_PATHS=/docs,/redoc,/openapi.json,/

# seconds between requests per IP
RATE_LIMIT_INTERVAL=1
```
