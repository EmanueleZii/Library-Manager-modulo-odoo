from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Libro'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # abilita chatter + log

    name = fields.Char(string='Titolo', required=True, tracking=True)
    author = fields.Char(string='Autore', required=True)
    isbn = fields.Char(string='ISBN')
    year = fields.Integer(string='Anno di pubblicazione')
    state = fields.Selection(
        selection=[
            ('available', 'Disponibile'),
            ('on_loan', 'In prestito'),
        ],
        string='Stato',
        default='available',
        tracking=True,
    )
    loan_ids = fields.One2many(
        comodel_name='library.loan',
        inverse_name='book_id',
        string='Prestiti',
    )
    loan_count = fields.Integer(
        string='N° Prestiti',
        compute='_compute_loan_count',
        store=True,
    )

    @api.depends('loan_ids')
    def _compute_loan_count(self):
        for book in self:
            book.loan_count = len(book.loan_ids)

    @api.constrains('year')
    def _check_year(self):
        for book in self:
            if book.year and book.year < 1400:
                raise ValidationError('Anno non valido. I libri stampati esistono dal 1400..')

    def action_view_loans(self):
        """Smart button → apre i prestiti del libro"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Prestiti',
            'res_model': 'library.loan',
            'view_mode': 'list,form',
            'domain': [('book_id', '=', self.id)],
        }
