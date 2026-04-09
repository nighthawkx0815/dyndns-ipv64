FROM python:3.12-alpine
WORKDIR /app
RUN pip install requests schedule
COPY ddns.py .
CMD ["python", "ddns.py"]
