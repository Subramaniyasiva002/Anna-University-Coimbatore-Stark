import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '#Sr@030')
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'auth_login'
