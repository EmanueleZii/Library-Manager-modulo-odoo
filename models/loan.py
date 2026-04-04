from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Prestito Libro'
    _inherit = ['mail.thread']

    book_id = fields.Many2one(
        comodel_name='library.book',
        string='Libro',
        required=True,
        ondelete='restrict',
    )
    
    #persona che ha pèreso in prestito il libro
    borrower_id = fields.Many2one(
        comodel_name='res.partner',
        string='Lettore',
        required=True,
    )
    loan_date = fields.Date(
        string='Data Prestito',
        default=fields.Date.today,
        required=True,
    )
    return_date = fields.Date(string='Data Restituzione')
    state = fields.Selection(
        selection=[
            ('active', 'Attivo'),
            ('returned', 'Restituito'),
        ],
        string='Stato',
        default='active',
        tracking=True,
    )
    
    #calcola se e in ritardo la consegna del libro prestato
    is_overdue = fields.Boolean(
        string='In Ritardo',
        compute='_compute_is_overdue',
    )

    #calcola se il prestito e in ritardo
    @api.depends('return_date', 'state')
    def _compute_is_overdue(self):
        today = date.today()
        for loan in self:
             if loan.state == 'active' and bool(loan.return_date) and loan.return_date < today:
                loan.is_overdue = True
            else:
                loan.is_overdue = False

    def action_return(self):
        """Bottone 'Restituisci': chiude il prestito e libera il libro"""
        for loan in self:
            if loan.state == 'returned':
                raise UserError('Prestito già restituito.')
            loan.state = 'returned'
            loan.book_id.state = 'available'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for loan in records:
            if loan.book_id.state != 'available':
                raise UserError(
                    f'Il libro "{loan.book_id.name}" non è disponibile.'
                )
            loan.book_id.state = 'on_loan'
        return records
