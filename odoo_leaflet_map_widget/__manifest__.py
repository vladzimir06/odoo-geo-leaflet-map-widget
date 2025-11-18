{
    'name': "Odoo Geo Leaflet Map Widget",
    'summary': "Reusable Leaflet map widget for Odoo forms.",
    'description': "Provides a custom field widget based on Leaflet for manual coordinate selection and reverse geocoding.",
    'author': "vladzimir06",
    'category': 'Extra Tools',
    'version': '19.0.1.0.0',

    'depends': ['web', 'base'],

    'external_dependencies': {
        'python': ['geopy'],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/map_viewer_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # Leaflet from CDN
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',

            # Widget files
            'odoo_leaflet_map_widget/static/src/js/geo_leaflet_map.js',
            'odoo_leaflet_map_widget/static/src/xml/geo_leaflet_map.xml',
            'odoo_leaflet_map_widget/static/src/css/geo_leaflet_map.css',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
