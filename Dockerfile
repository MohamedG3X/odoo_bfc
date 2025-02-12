FROM odoo:12

# Set environment variables for PostgreSQL connection
ENV DB_HOST="roundhouse.proxy.rlwy.net" \
    DB_PORT="41835" \
    DB_USER="postgres" \
    DB_PASSWORD="cJgQzjWqlWbcojdfgIvEtmCcFJIRoTJo" \
    DB_NAME="railway"

# Expose Odoo port
EXPOSE 8069

# Run Odoo with correct database connection settings
CMD ["odoo", "--db_host=roundhouse.proxy.rlwy.net", "--db_port=41835", "--db_user=postgres", "--db_password=cJgQzjWqlWbcojdfgIvEtmCcFJIRoTJo", "--db_name=railway"]
