from sqlmodel import SQLModel
from app.atlas_models import User, Post
from atlas_provider_sqlalchemy.ddl import print_ddl

def generate_ddl():
    print_ddl("postgresql", [User, Post])

if __name__ == "__main__":
    generate_ddl()
