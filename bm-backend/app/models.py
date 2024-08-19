from sqlalchemy import Column, Integer, String, Table
from app.db import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(120), unique=True, index=True),
    Column("name", String(120)),
    Column("picture", String(200)),
)