"""fundamental-tables

Revision ID: 99b1175dd6db
Revises:
Create Date: 2022-10-19 13:58:18.381533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99b1175dd6db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql_batch = """
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    CREATE TABLE IF NOT EXISTS identity_media (
        uuid UUID DEFAULT uuid_generate_v1() PRIMARY KEY,
        name VARCHAR(255),
        type VARCHAR(255),
        content BYTEA,
        length INTEGER,
        content_extract BYTEA,
        extract_length INTEGER,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );
    """
    op.execute(sql_batch)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS identity_media;")
