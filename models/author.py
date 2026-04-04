from odoo import models, fields


class Author(models.Model):
    """
    Modello Autore.
    Relazione: un autore può avere molti libri (one2many).
    """
    _name = 'library.author'
    _description = 'Autore'
    _order = 'name'

    name = fields.Char(string='Nome', required=True)
    bio = fields.Text(string='Biografia')
    birth_date = fields.Date(string='Data di nascita')

    # Computed field: conta i libri dell'autore
    book_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='author_id',
        string='Libri'
    )
    book_count = fields.Integer(
        string='N° Libri',
        compute='_compute_book_count',
        store=True,
    )
    
    @api.depends('book_ids')
    def _compute_book_count(self):
        """Ricalcola il numero di libri per ogni autore."""
        for author in self:
            author.book_count = len(author.book_ids)
