FROM odoo:12

# Set environment variables for PostgreSQL connection
ENV DB_HOST="postgres.railway.internal" \
    DB_PORT="5432" \
    DB_USER="postgres" \
    DB_PASSWORD="cJgQzjWqlWbcojdfgIvEtmCcFJIRoTJo" \
    DB_NAME="railway"

# Expose Odoo port
EXPOSE 8069

# Run Odoo with correct database connection settings
CMD ["odoo", "--db_host=postgres.railway.internal", "--db_port=5432", "--db_user=postgres", "--db_password=cJgQzjWqlWbcojdfgIvEtmCcFJIRoTJo", "--db_name=railway"]
