# تصویر پایه سبک پایتون
FROM python:3.12-slim

# دایرکتوری کاری داخل کانتینر
WORKDIR /code

# کپی فایل وابستگی‌ها و نصبشون
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# کپی کد پروژه
COPY app /code/app

# پورت 8000 رو باز کن
EXPOSE 8000

# دستور اجرا
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
