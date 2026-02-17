"""Atlas SQLAlchemy provider entrypoint.

SQLModel is SQLAlchemy-based; importing models populates SQLModel.metadata.
"""

from .models import Post, User  # noqa: F401
from sqlmodel import SQLModel

metadata = SQLModel.metadata
