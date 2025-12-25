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

# واحدهای پشتیبانی‌شده
LENGTH_UNITS = {"meter", "kilometer", "centimeter", "inch", "foot"}
TEMP_UNITS = {"celsius", "fahrenheit", "kelvin"}

# تبدیل طول: همه به متر
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

# تبدیل دما: همه از/به سلسیوس
def celsius_to(target: str, celsius: float) -> float:
    if target == "celsius":
        return celsius
    elif target == "fahrenheit":
        return celsius * 9/5 + 32
    elif target == "kelvin":
        return celsius + 273.15

def to_celsius(source: str, value: float) -> float:
    if source == "celsius":
        return value
    elif source == "fahrenheit":
        return (value - 32) * 5/9
    elif source == "kelvin":
        return value - 273.15

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in TEMP_UNITS or to_unit not in TEMP_UNITS:
        raise HTTPException(status_code=400, detail="واحد دما نامعتبر است")
    celsius = to_celsius(from_unit, value)
    result = celsius_to(to_unit, celsius)
    return round(result, 6)

@app.get("/")
def root():
    return {"message": "Unit Converter API is running!"}

@app.post("/convert")
async def convert(request: ConvertRequest):
    # تشخیص نوع واحد (طول یا دما)
    if request.from_unit in LENGTH_UNITS and request.to_unit in LENGTH_UNITS:
        result = convert_length(request.value, request.from_unit, request.to_unit)
        return {"result": result, "unit": request.to_unit}
    
    elif request.from_unit in TEMP_UNITS and request.to_unit in TEMP_UNITS:
        result = convert_temperature(request.value, request.from_unit, request.to_unit)
        return {"result": result, "unit": request.to_unit}
    
    else:
        raise HTTPException(
            status_code=400,
            detail="واحدهای مبدأ و مقصد باید هر دو از نوع طول یا هر دو از نوع دما باشند"
        )
