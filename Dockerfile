FROM apache/superset:latest

EXPOSE 8088

USER root
COPY superset_config.py /app/pythonpath/superset_config.py
COPY entrypoint.sh /app/entrypoint.sh

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN chmod +x /app/entrypoint.sh
USER superset

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8088