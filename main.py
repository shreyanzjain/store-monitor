from fastapi import FastAPI, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src import models, schemas
import pandas as pd
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/upload/')
def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file.file)
    except:
        return HTTPException(status_code=400, detail="Bad Request: Invalid File")
    
    for _, row in df.iterrows():
        new_status_entry = schemas.StatusByTimeCreate(store_id=row["store_id"],
                                                timestamp_utc=datetime.strptime(row["timestamp_utc"],
                                                '%Y-%m-%d %H:%M:%S.%f %Z'),
                                                status=row["status"])
        new_status_entry_model = models.StatusByTime(**new_status_entry.dict())
        # if(db.query(models.StatusByTime).filter(
        #     models.StatusByTime.timestamp_utc == new_status_entry_model.timestamp_utc,
        #     models.StatusByTime.store_id == new_status_entry_model.store_id)):
        #     pass
        # else:
        db.add(new_status_entry_model)
        db.commit()
        db.refresh(new_status_entry_model)
        
    return new_status_entry