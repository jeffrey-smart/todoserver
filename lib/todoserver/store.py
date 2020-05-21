# lib/todoserver/store.py

from sqlalchemy import(
    create_engine,
    Column,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'                     # create the table
    id = Column(Integer, primary_key=True)      # add `id` to table
    summary = Column(String)                    # add `string` to table
    description = Column(String)                # add `description` to table

class TaskStore:
    def __init__(self, engine_spec):
        self.engine = create_engine(engine_spec)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_all_tasks(self):
        return [
            { "id": task.id, "summary": task.summary }
            for task in self.Session().query(Task).all()
        ]

    def create_task(self, summary, description):
        session = self.Session()
        task = Task(summary=summary, description=description)
        session.add(task)
        session.commit()
        return task.id

    def task_details(self, task_id):
        task = self.Session().query(Task).get(task_id)

        if task is None:
            return None

        return {
            "id": task.id,
            "summary": task.summary,
            "description": task.description
        }

    def _delete_all_tasks(self):
        session = self.Session()
        session.query(Task).delete()
        session.commit()

    def delete_task(self, task_id):
        session = self.Session()
        task = session.query(Task).get(task_id)
        session.delete(task)
        session.commit()

