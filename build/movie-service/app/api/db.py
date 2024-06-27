import os
from base64 import b64decode

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, ARRAY)
from databases import Database

# Récupérer les informations de connexion à partir des variables d'environnement
postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_db_movie = os.environ.get('POSTGRES_DB_MOVIE')
postgres_host = os.environ.get('POSTGRES_HOST')
postgres_port = os.environ.get('POSTGRES_PORT')

DATABASE_URI = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_movie}"

# Créer un moteur SQLAlchemy
engine = create_engine(DATABASE_URI)

metadata = MetaData()

movies = Table(
    'movies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', ARRAY(String)),
    Column('casts_id', ARRAY(Integer))
)

database = Database(DATABASE_URI)
