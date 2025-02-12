import base64
import qrcode
from io import BytesIO
from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class MartialArtsCenter(models.Model):
    _name = 'martial.arts.center'
    _description = 'Martial Arts Center Member Management'
    _inherit = ['mail.thread']

    name = fields.Char(string='Member Name', required=True, track_visibility="onchange")
    sequence = fields.Char(string='Member ID', copy=False, readonly=True)
    contact_info = fields.Char(string='Contact Information', track_visibility="onchange")
    photo = fields.Binary(string='Photo')
    subscription_start = fields.Date(string='Subscription Start Date', default=fields.Date.today,
                                     track_visibility="onchange")
    subscription_end = fields.Date(string='Subscription End Date')
    subscription_duration = fields.Selection([
        ('1', '1 Month'),
        ('2', '2 Months'),
        ('3', '3 Months'),
        ('6', '6 Months'),
        ('12', '12 Months'),
    ], string='Subscription Duration', default='1', required=True, track_visibility="onchange")
    subscription_status = fields.Selection([
        ('active', 'Active - صالح'),
        ('expired', 'Expired -منتهي')
    ], string='Subscription Status', compute='_compute_subscription_status', store=True, track_visibility="onchange")

    game_ids = fields.Many2many('martial.arts.game', string='Selected Games')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    number_of_attend = fields.Integer(string="Attends-عدد الحضور", tracking=True, track_visibility="onchange")
    number_of_session = fields.Integer(string="Number of Session-عدد التمرينات المدفوعه", tracking=True, track_visibility="onchange")
    remaining_sessions = fields.Integer(string="Remaining Sessions-عدد التمرينات المتبقيه", compute='_compute_remaining_sessions', store=True, track_visibility="onchange")
    contact_info_readonly = fields.Char(
        string='Contact Info (Read-Only)',
        related='contact_info',
        readonly=True
    )

    @api.model
    def create(self, vals):
        # Generate the sequence number
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('martial.arts.center.sequence') or 'BFC001'
        return super(MartialArtsCenter, self).create(vals)

    @api.depends('subscription_start', 'subscription_end', 'number_of_attend', 'number_of_session')
    def _compute_subscription_status(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.subscription_end and record.subscription_end >= today and record.number_of_attend < record.number_of_session:
                record.subscription_status = 'active'
            else:
                record.subscription_status = 'expired'

    @api.onchange('subscription_duration', 'subscription_start')
    def _compute_subscription_end(self):
        for record in self:
            if record.subscription_start:
                duration = int(record.subscription_duration)
                record.subscription_end = record.subscription_start + timedelta(days=duration * 30)

    @api.depends('game_ids')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(game.price for game in record.game_ids)

    @api.depends('number_of_attend', 'number_of_session')
    def _compute_remaining_sessions(self):
        for record in self:
            record.remaining_sessions = max(0, record.number_of_session - record.number_of_attend)

    def increment_attendance(self):
        for record in self:
            if record.number_of_attend >= record.number_of_session:
                raise ValidationError("The subscription is expired. You cannot attend more sessions.")
            record.number_of_attend += 1
            if record.number_of_attend >= record.number_of_session:
                record.subscription_status = 'expired'

    # Method to generate QR code for contact_info_readonly
    def generate_qr_code(self):
        """Generate a QR code for the contact_info_readonly field and return it as a base64-encoded image."""
        if self.contact_info_readonly:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.contact_info_readonly)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
        return ""


class MartialArtsGame(models.Model):
    _name = 'martial.arts.game'
    _description = 'Martial Arts Games'

    name = fields.Char(string='Game Name', required=True)
    price = fields.Float(string='Price')
    photo = fields.Binary(string=" Photo", attachment=True)


class MartialArtsRenewal(models.Model):
    _name = 'martial.renewal.game'
    _description = 'Martial Arts Subscription Renewal'

    member_id = fields.Many2one('martial.arts.center', string='Member', required=True)
    renewal_time = fields.Selection([
        ('1', '1 Month'),
        ('2', '2 Months'),
        ('3', '3 Months'),
        ('6', '6 Months'),
        ('12', '12 Months'),
    ], string='Subscription Renewal', default='1', required=True)
    renewal_date = fields.Date(string='Renewal-Date', default=fields.Date.today, readonly="1")
    renewal_session = fields.Integer(string='Renewal-Session')

    @api.model
    def create(self, vals):
        record = super(MartialArtsRenewal, self).create(vals)
        record._update_subscription_end()
        return record

    def write(self, vals):
        result = super(MartialArtsRenewal, self).write(vals)
        self._update_subscription_end()
        return result

    def _update_subscription_end(self):
        for record in self:
            if record.member_id:
                renewal_date = record.renewal_date or fields.Date.context_today(self)
                member = record.member_id
                member.subscription_start = renewal_date
                duration = int(record.renewal_time)
                member.subscription_end = renewal_date + timedelta(days=duration * 30)
                member.subscription_duration = record.renewal_time
                member.number_of_attend = 0
                member.number_of_session = record.renewal_session
                member._compute_subscription_status()
