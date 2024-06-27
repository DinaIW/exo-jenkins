import os
from base64 import b64decode

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, ARRAY)
from databases import Database

# Récupérer les informations de connexion à partir des variables d'environnement
postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_db_cast = os.environ.get('POSTGRES_DB_CAST')
postgres_host = os.environ.get('POSTGRES_HOST')
postgres_port = os.environ.get('POSTGRES_PORT')

DATABASE_URI = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_cast}"
print(postgres_db_cast)

# Créer un moteur SQLAlchemy
engine = create_engine(DATABASE_URI)

metadata = MetaData()

casts = Table(
    'casts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('nationality', String(20)),
)

database = Database(DATABASE_URI)
