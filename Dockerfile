FROM python:3.12
WORKDIR /opt/app
COPY app.py check.py ledger ./
COPY samples/ /opt/samples/
COPY probe.py /tmp/probe.py
ENV LEDGER_VERSION=1.0.0
EXPOSE 8080
HEALTHCHECK CMD python /tmp/probe.py
CMD ["python", "app.py"]
