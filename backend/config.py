import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/workshop_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
