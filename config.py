import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambia-esto-por-una-clave-secreta'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///piscicola.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
