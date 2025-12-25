from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Unit Converter Microservice",
    description="تبدیل واحدهای دما و طول - شماره دانشجویی: ۱۴۰۱۵۳۶۱۹۲۲"
)

class ConvertRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str

@app.get("/")
def root():
    return {"message": "Unit Converter API is running!"}
