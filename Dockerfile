FROM odoo:12

# Set environment variables for PostgreSQL connection
ENV HOST=postgres.railway.internal \
    PORT=5432 \
    USER=postgres \
    PASSWORD=cJgQzjWqlWbcojdfgIvEtmCcFJIRoTJo \
    DATABASE=railway

# Set file permissions
RUN chown -R odoo /mnt/extra-addons

# Expose Odoo's default port
EXPOSE 8069

# Start Odoo
CMD ["odoo", "--db_host=postgres.railway.internal", "--db_port=5432", "--db_user=postgres", "--db_password=cJgQzjWqlWbcojdfgIvEtmCcFJIRoTJo", "--db_name=railway"]
