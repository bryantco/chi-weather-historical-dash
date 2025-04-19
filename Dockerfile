FROM apache/superset:latest
USER root

EXPOSE 8088

######################################################################
# Copy dashboards
######################################################################
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER superset

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8088