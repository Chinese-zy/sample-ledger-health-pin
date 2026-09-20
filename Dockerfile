FROM python:3.12 AS builder
WORKDIR /build
ARG LEDGER_VERSION=
COPY check.py ./check.py
COPY ledger/books.json ./ledger/books.json
RUN python check.py ledger/books.json dist/books.json "${LEDGER_VERSION}"

FROM python:3.12
WORKDIR /opt/app
COPY --from=builder /build/dist/books.json ./books.json
COPY --from=builder /build/dist/books.version ./books.version
COPY app.py ./app.py
COPY probe.py /tmp/probe.py
EXPOSE 8080
HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD ["python", "/tmp/probe.py"]
CMD ["python", "app.py"]
