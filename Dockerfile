FROM apache/superset:latest

USER root
COPY superset_config.py /app/pythonpath/superset_config.py
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
USER superset

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8088