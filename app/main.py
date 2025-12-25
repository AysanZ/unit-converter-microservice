from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Unit Converter Microservice",
    description="تبدیل واحدهای دما و طول - شماره دانشجویی: ۱۴۰۱۵۳۶۱۹۲۲"
)

class ConvertRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str

# لیست واحدهای طول
LENGTH_UNITS = {"meter", "kilometer", "centimeter", "inch", "foot"}

# ضریب تبدیل همه به متر
TO_METER = {
    "meter": 1,
    "kilometer": 1000,
    "centimeter": 0.01,
    "inch": 0.0254,
    "foot": 0.3048
}

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in LENGTH_UNITS or to_unit not in LENGTH_UNITS:
        raise HTTPException(status_code=400, detail="واحد طول نامعتبر است")
    
    meters = value * TO_METER[from_unit]
    result = meters / TO_METER[to_unit]
    return round(result, 6)

@app.get("/")
def root():
    return {"message": "Unit Converter API is running!"}

@app.post("/convert")
async def convert(request: ConvertRequest):
    if request.from_unit in LENGTH_UNITS and request.to_unit in LENGTH_UNITS:
        result = convert_length(request.value, request.from_unit, request.to_unit)
        return {"result": result, "unit": request.to_unit}
    
    raise HTTPException(status_code=400, detail="فقط تبدیل واحدهای طول در این نسخه پشتیبانی می‌شود")
