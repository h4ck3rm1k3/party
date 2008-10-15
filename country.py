#This file is part of Tryton.  The COPYRIGHT file at the top level of this repository contains the full copyright notices and license terms.
from trytond.osv import fields, OSV
STATES = {
    'readonly': "active == False",
}


class Country(OSV):
    'Country'
    _name = 'relationship.country'
    _description = __doc__
    name = fields.Char('Name', required=True, translate=True,
           help='The full name of the country.', select=1)
    code = fields.Char('Code', size=2, select=1,
           help='The ISO country code in two chars.\n'
           'You can use this field for quick search.', required=True)
    subdivisions = fields.One2Many('relationship.country.subdivision',
            'country', 'Subdivisions')

    def __init__(self):
        super(Country, self).__init__()
        self._sql_constraints += [
            ('name_uniq', 'UNIQUE(name)',
             'The name of the country must be unique!'),
            ('code_uniq', 'UNIQUE(code)',
             'The code of the country must be unique!'),
        ]
        self._order.insert(0, ('code', 'ASC'))

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=None):
        if not args:
            args=[]
        ids = False
        if len(name) <= 2:
            ids = self.search(cr, user, [('code', '=', name.upper())] + args,
                    limit=limit, context=context)
        if not ids:
            ids = self.search(cr, user, [('name', operator, name)] + args,
                    limit=limit, context=context)
        return self.name_get(cr, user, ids, context)

    def create(self, cursor, user, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        new_id = super(Country, self).create(cursor, user, vals, context=context)
        if 'module' in context:
            cursor.execute('INSERT INTO ir_translation ' \
                    '(name, lang, type, src, res_id, value, module, fuzzy) ' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, false)',
                    ('relationship.country,name', 'en_US', 'model',
                        vals['name'], new_id, '', context.get('module')))
        return new_id

    def write(self, cursor, user, ids, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(Country, self).write(cursor, user, ids, vals,
                context=context)

Country()


class Subdivision(OSV):
    "Subdivision"
    _name = 'relationship.country.subdivision'
    _description = __doc__
    country = fields.Many2One('relationship.country', 'Country',
            required=True)
    name = fields.Char('Name', required=True, select=1)
    code = fields.Char('Code', required=True, select=1)
    type = fields.Selection([
        ('administration', 'Administration'),
        ('administrative area', 'Administrative area'),
        ('administrative region', 'Administrative Region'),
        ('administrative territory', 'Administrative Territory'),
        ('area', 'Area'),
        ('atoll', 'Atoll'),
        ('autonomous city', 'Autonomous City'),
        ('autonomous commune', 'Autonomous Commune'),
        ('autonomous communities', 'Autonomous communities'),
        ('autonomous district', 'Autonomous District'),
        ('autonomous island', 'Autonomous island'),
        ('autonomous monastic state', 'Autonomous monastic state'),
        ('autonomous municipality', 'Autonomous municipality'),
        ('autonomous province', 'Autonomous Province'),
        ('autonomous region', 'Autonomous Region'),
        ('autonomous republic', 'Autonomous republic'),
        ('autonomous sector', 'Autonomous sector'),
        ('autonomous territory', 'Autonomous territory'),
        ('borough', 'Borough'),
        ('canton', 'Canton'),
        ('capital city', 'Capital city'),
        ('capital district', 'Capital District'),
        ('capital metropolitan city', 'Capital Metropolitan City'),
        ('capital territory', 'Capital Territory'),
        ('city', 'City'),
        ('city corporation', 'City corporation'),
        ('city with county rights', 'City with county rights'),
        ('commune', 'Commune'),
        ('country', 'Country'),
        ('county', 'County'),
        ('department', 'Department'),
        ('dependency', 'Dependency'),
        ('district', 'District'),
        ('division', 'Division'),
        ('economic prefecture', 'Economic Prefecture'),
        ('economic region', 'Economic region'),
        ('emirate', 'Emirate'),
        ('entity', 'Entity'),
        ('federal dependency', 'Federal Dependency'),
        ('federal district', 'Federal District'),
        ('federal territories', 'Federal Territories'),
        ('geographical region', 'Geographical region'),
        ('geographical unit', 'Geographical unit'),
        ('governorate', 'Governorate'),
        ('included for completeness', 'Included for completeness'),
        ('island council', 'Island council'),
        ('island group', 'Island group'),
        ('local council', 'Local council'),
        ('london borough', 'London borough'),
        ('metropolitan cities', 'Metropolitan cities'),
        ('metropolitan department', 'Metropolitan department'),
        ('metropolitan district', 'Metropolitan district'),
        ('metropolitan region', 'Metropolitan region'),
        ('municipalities', 'Municipalities'),
        ('municipality', 'Municipality'),
        ('oblast', 'Oblast'),
        ('outlying area', 'Outlying area'),
        ('overseas region/department', 'Overseas region/department'),
        ('overseas territorial collectivity', 'Overseas territorial collectivity'),
        ('parish', 'Parish'),
        ('prefecture', 'Prefecture'),
        ('principality', 'Principality'),
        ('province', 'Province'),
        ('rayon', 'Rayon'),
        ('region', 'Region'),
        ('regional council', 'Regional council'),
        ('republic', 'Republic'),
        ('special administrative region', 'Special administrative region'),
        ('special city', 'Special city'),
        ('special district', 'Special District'),
        ('special municipality', 'Special Municipality'),
        ('special region', 'Special Region'),
        ('special zone', 'Special zone'),
        ('state', 'State'),
        ('territorial unit', 'Territorial unit'),
        ('territory', 'Territory'),
        ('town council', 'Town council'),
        ('two-tier county', 'Two-tier county'),
        ('union territory', 'Union territory'),
        ('unitary authority', 'Unitary authority'),
        ], 'Type', required=True)
    parent = fields.Many2One('relationship.country.subdivision', 'Parent')

    def __init__(self):
        super(Subdivision, self).__init__()
        self._order.insert(0, ('code', 'ASC'))

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=None):
        if not args:
            args=[]
        ids = self.search(cr, user, [('code', '=', name.upper())] + args,
                limit=limit, context=context)
        if not ids:
            ids = self.search(cr, user, [('name', operator, name)] + args,
                    limit=limit, context=context)
        return self.name_get(cr, user, ids, context)

    def create(self, cursor, user, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(Subdivision, self).create(cursor, user, vals,
                context=context)

    def write(self, cursor, user, ids, vals, context=None):
        if 'code' in vals:
            vals['code'] = vals['code'].upper()
        return super(Subdivision, self).write(cursor, user, ids, vals,
                context=context)

Subdivision()
