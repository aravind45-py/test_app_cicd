FROM python:3.11.9-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["fastapi","run"]