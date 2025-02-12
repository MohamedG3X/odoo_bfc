FROM odoo:12

# Set working directory
WORKDIR /mnt/extra-addons

# Copy your custom module to Odoo addons path
COPY ./odoo/custom_addons /mnt/extra-addons

# Expose the Odoo port
EXPOSE 8069

# Start Odoo
CMD ["odoo", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"]
