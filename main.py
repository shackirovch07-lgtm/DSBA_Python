from fastapi import FastAPI,Depends
from sqlmodel import create_engine
from sqlmodel import SQLModel, Field,Session, select
from contextlib import asynccontextmanager
engine = create_engine("sqlite:///university.db")

class University(SQLModel, table=True):
    id : int = Field(primary_key=True,default=None)
    name : str
    city : str
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def main_page():
    return "Hello"

@app.post("/university")
def add_uni(university : University, session : Session=Depends(get_session)):
    session.add(university)
    session.commit()
    session.refresh(university)
    print(university)

@app.get("/universities")
def get_all_uni(session : Session=Depends(get_session)):
    return session.exec(select(University)).first()
