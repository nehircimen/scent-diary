FROM python:3.13-slim
WORKDIR /app
COPY project.py schema.sql ./
CMD ["python", "project.py"]
