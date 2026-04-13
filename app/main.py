from app.db import engine
from app.models import metadata, tasks
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Create tables in the database
metadata.create_all(engine)


# Get all tasks from the database
def get_all_tasks():
    with engine.connect() as conn:
        try:
            # Select all rows from tasks table
            query = select(tasks)
            result = conn.execute(query)

            # Convert each row to dictionary
            data = [dict(row._mapping) for row in result]
            return data
        
        except SQLAlchemyError:
            conn.rollback()
            raise


# Insert a new task
def insert_task(name):
    with engine.connect() as conn:
        try:
            # Insert task name into table
            query = insert(tasks).values(name = name)
            result = conn.execute(query)

            # Save changes
            conn.commit()

            # Return inserted task ID
            return result.inserted_primary_key[0]
        
        except SQLAlchemyError as e:
            conn.rollback()
            raise


# Delete a task by ID
def delete_task(id):
    with engine.connect() as conn:
        try:
            # Delete task where id matches
            query = delete(tasks).where(tasks.c.id == id)
            result = conn.execute(query)

            # Save changes
            conn.commit()

            # Return number of rows deleted
            return result.rowcount
        
        except SQLAlchemyError:
            conn.rollback()
            raise


# Update a task name by ID
def update_task(id, new_name):
    with engine.connect() as conn:
        try:
            # Update task name where id matches
            query = update(tasks).where(tasks.c.id == id).values(name = new_name)
            result = conn.execute(query)

            # Save changes
            conn.commit()

            # Return number of rows updated
            return result.rowcount
        
        except SQLAlchemyError:
            conn.rollback()
            raise


# Get a single task by ID
def get_task_by_id(id):
    with engine.connect() as conn:
        try:
            # Select task where id matches
            query = select(tasks).where(tasks.c.id == id)
            result = conn.execute(query).first()

            # Convert row to dictionary
            return dict(result._mapping)

        except SQLAlchemyError:
            conn.rollback()
            raise