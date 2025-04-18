FROM apache/superset:latest

EXPOSE 8088

######################################################################
# Copy dashboards
######################################################################
COPY dashboards /app/dashboards
COPY charts /app/charts
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8088