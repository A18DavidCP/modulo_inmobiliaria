# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class InmobiliariaCasa(models.Model):
    _name = 'inmobiliaria.casa'
    _description = 'Casa'

    id_casa = fields.Char('ID', required=True)
    fecha_const = fields.Date('Fecha de construccion')
    metros_cuadrados = fields.Integer('Metros cuadrados')
    precio_compra = fields.Integer('Venta')
    num_habitaciones = fields.Integer('Habitaciones')
    state = fields.Selection([
        ('disponible', 'Disponible'),
        ('reforma', 'Reforma'),
        ('vendida', 'Vendida')],
        'Disponibilidad', default="disponible")
        
    esta_vendida = fields.Boolean('Vendida', compute='check_venta', default=False)

    @api.multi
    def check_venta(self):
        for casa in self:
            domain = [('casa_id.id', '=', casa.id)]
            casa.esta_vendida = self.env['inmobiliaria.contrato'].search(domain, count=True) > 1                
        
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('disponible', 'reforma'),
                   ('disponible', 'vendida'),
                   ('reforma', 'disponible')]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for casa in self:
            if casa.is_allowed_transition(casa.state, new_state):
                casa.state = new_state
            else:
                message = _('No se puede pasar de %s a %s') % (casa.state, new_state)
                raise UserError(message)

    def make_available(self):
        self.change_state('disponible')

    def make_reforma(self):
        self.change_state('reforma')
        
    def make_venta(self):
        self.change_state('vendida')

    @api.multi
    def change_update_date(self):
        self.ensure_one()
        self.date_updated = fields.Datetime.now()

class InmobiliariaPersona(models.Model):
    _name = 'inmobiliaria.persona'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    member_number = fields.Char()
    tipo_persona =fields.Selection([ 
        ('agente', 'Agente'),
        ('cliente', 'Cliente')],
        'Tipo', default="cliente")
    date_of_birth = fields.Date('Fecha nacimiento')


class InmobiliariaContrato(models.Model):
    _name = 'inmobiliaria.contrato'
    _description = 'Contrato inmobiliaria'
    _rec_name = 'casa_id'
    _order = 'casa_id desc'

    cliente = fields.Many2one('inmobiliaria.persona', required=True)
    casa_id =  fields.Many2one('inmobiliaria.casa', required=True)
    meses_pago = fields.Integer('Numero de meses pago')
    @api.one
    def _get_total(self):
    
        self.pago_mensual = self.casa_id.precio_compra / self.meses_pago
        
            
    pago_mensual = fields.Float(compute='_get_total', string="Pago mensual")
    date_start = fields.Date('Inicio Contrato')


    @api.constrains('casa_id')
    def _check_casa_id(self):
       for contrato in self:
            casa = contrato.casa_id
            domain = [('casa_id.id', '=', casa.id)]           
            contrato.esta_vendida = self.search(domain, count=True) > 1 
            if casa.esta_vendida:
                raise models.ValidationError('Casa vendida') 
                
    @api.constrains('date_start')
    def _check_dates(self):
        for contrato in self:
            if contrato.casa_id.fecha_const > contrato.date_start:
                raise models.ValidationError('Casa sin construir')