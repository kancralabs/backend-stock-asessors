import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_database_connection(db_session: AsyncSession):
    """
    Test database connection
    """
    result = await db_session.execute(text("SELECT 1"))
    value = result.scalar()
    assert value == 1


@pytest.mark.asyncio
async def test_database_transaction(db_session: AsyncSession):
    """
    Test database transaction
    """
    # Create a temporary table
    await db_session.execute(
        text("CREATE TEMP TABLE test_table (id INTEGER, name TEXT)")
    )
    await db_session.commit()

    # Insert data
    await db_session.execute(
        text("INSERT INTO test_table (id, name) VALUES (1, 'test')")
    )
    await db_session.commit()

    # Query data
    result = await db_session.execute(text("SELECT * FROM test_table WHERE id = 1"))
    row = result.fetchone()
    assert row is not None
    assert row[0] == 1
    assert row[1] == "test"


@pytest.mark.asyncio
async def test_database_rollback(db_session: AsyncSession):
    """
    Test database rollback
    """
    # Create a temporary table
    await db_session.execute(
        text("CREATE TEMP TABLE test_rollback (id INTEGER, name TEXT)")
    )
    await db_session.commit()

    # Insert data but rollback
    await db_session.execute(
        text("INSERT INTO test_rollback (id, name) VALUES (1, 'test')")
    )
    await db_session.rollback()

    # Query data - should be empty
    result = await db_session.execute(text("SELECT COUNT(*) FROM test_rollback"))
    count = result.scalar()
    assert count == 0
