FROM python:3.10-slim
RUN pip install flask cloudscraper
COPY proxy.py .
CMD ["python", "proxy.py"]
