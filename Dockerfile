FROM odoo:12

# Set working directory
WORKDIR /mnt/extra-addons

# Set environment variables for PostgreSQL connection
ENV HOST=db \
    PORT=5432 \
    USER=postgres \
    PASSWORD=cJgQzjWqlWbcojdfgIvEtmCcFJIRoTJo \
    DATABASE=railway

# Copy your custom module to Odoo addons path (Uncomment if needed)
# COPY ./odoo/custom_addons /mnt/extra-addons

# Set file permissions
RUN chown -R odoo /mnt/extra-addons

# Expose Odoo's default port
EXPOSE 8069

# Start Odoo with the correct database host
CMD ["odoo", "--db_host=db", "--db_port=5432", "--db_user=postgres", "--db_password=cJgQzjWqlWbcojdfgIvEtmCcFJIRoTJo", "--db_name=railway", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/od
