FROM python:3.9.7

WORKDIR /usr/src/sysprofile

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./* .

CMD ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "8000"]