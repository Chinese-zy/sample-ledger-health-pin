FROM python:3.12
WORKDIR /opt/app
COPY app.py check.py ledger ./
COPY probe.py /tmp/probe.py
EXPOSE 8080
HEALTHCHECK CMD python /tmp/probe.py
CMD ["python", "app.py"]
