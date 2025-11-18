from odoo import api, fields, models, _
import time
try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
except ImportError:
    Nominatim = None
    GeocoderTimedOut = None
    GeocoderServiceError = None
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class MapViewer(models.Model):
    _name = 'map.viewer'
    _description = 'Leaflet Map Viewer Example'

    # Manual map coordinates
    map_latitude = fields.Float(
        string='Map Latitude',
        digits=(16, 5),
        help="Latitude selected manually on the map."
    )
    map_longitude = fields.Float(
        string='Map Longitude',
        digits=(16, 5),
        help="Longitude selected manually on the map."
    )
    map_canvas = fields.Char(string='Map View')  # Placeholder for widget

    # Helper fields
    partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    country_id = fields.Many2one('res.country', string='Country')
    city = fields.Char(string='City')
    street = fields.Char(string='Street')
    zip = fields.Char(string='Zip')

    osm_map_url = fields.Char(string='OpenStreetMap', compute='_compute_map_links', store=False)

    @api.depends('partner_latitude', 'partner_longitude')
    def _compute_map_links(self):
        for rec in self:
            if rec.partner_latitude and rec.partner_longitude:
                lat = rec.partner_latitude
                lon = rec.partner_longitude
                rec.osm_map_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}"
            else:
                rec.osm_map_url = False

    def action_apply_partner_coordinates(self):
        """Apply coordinates selected on the map to the partner_* fields."""
        self.ensure_one()
        if self.map_latitude and self.map_longitude:
            self.partner_latitude = self.map_latitude
            self.partner_longitude = self.map_longitude
        else:
            raise UserError(_('Map coordinates are empty. Please select a point on the map first.'))

    def _reverse_geo_localize_osm(self, lat, lon):
        """Helper for reverse geocoding using OpenStreetMap (Nominatim)."""
        if not Nominatim:
            raise UserError(_("Python library 'geopy' is not installed."))
        try:
            geolocator = Nominatim(user_agent="Odoo_App")
            location = geolocator.reverse((lat, lon), exactly_one=True, addressdetails=True, timeout=10)
            time.sleep(1)  # Respect Nominatim rate limits

            if location and location.raw:
                address = location.raw.get('address', {})
                data = {
                    'country_code': address.get('country_code', '').upper(),
                    'city': address.get('city') or address.get('town') or address.get('village'),
                    'street': address.get('road') or address.get('street'),
                    'zip': address.get('postcode'),
                }
                return data
        except Exception as e:
            _logger.warning("[GEO][Reverse] Reverse geolocalization failed for %s, %s: %s", lat, lon, e)
            raise UserError(_("Geocoding service failed or timed out. Check logs for details."))
        return {}

    def action_reverse_localize(self):
        """Reverse geocode and fill address fields from coordinates."""
        self.ensure_one()
        lat = self.partner_latitude or self.map_latitude
        lon = self.partner_longitude or self.map_longitude

        if not lat or not lon:
            raise UserError(_('Coordinates are missing. Please localize or select a point on the map first.'))

        address_data = self._reverse_geo_localize_osm(lat, lon)

        if address_data:
            country = self.env['res.country'].search([('code', '=', address_data.get('country_code'))], limit=1)
            vals = {
                'country_id': country.id if country else False,
                'city': address_data.get('city'),
                'street': address_data.get('street'),
                'zip': address_data.get('zip'),
            }
            vals = {k: v for k, v in vals.items() if v}
            self.write(vals)
        else:
            raise UserError(_('Failed to find address for the given coordinates.'))
