/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useRef, onMounted, onWillUnmount } from "@odoo/owl";

const DEFAULT_LAT = 55.751244;
const DEFAULT_LON = 37.617494;

export class GeoLeafletMap extends Component {
    setup() {
        this.mapRef = useRef("mapContainer");
        this.map = null;
        this.marker = null;

        onMounted(this.renderMap.bind(this));
        onWillUnmount(this.destroyMap.bind(this));
    }

    renderMap() {
        if (!window.L) {
            console.error("Leaflet library (L) is not loaded!");
            return;
        }

        const TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
        const ATTRIBUTION = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>';

        const recordData = this.props.record.data || {};

        const targetLat = recordData.partner_latitude;
        const targetLon = recordData.partner_longitude;

        const storedLat = recordData.map_latitude;
        const storedLon = recordData.map_longitude;

        let initialLat = targetLat || storedLat || DEFAULT_LAT;
        let initialLon = targetLon || storedLon || DEFAULT_LON;
        let initialZoom = 13;
        let hasInitialMarker = !!(targetLat || storedLat);

        const initialPosition = [initialLat, initialLon];

        this.map = L.map(this.mapRef.el).setView(initialPosition, initialZoom);

        L.tileLayer(TILE_URL, {
            attribution: ATTRIBUTION,
        }).addTo(this.map);

        if (hasInitialMarker) {
            this.marker = L.marker(initialPosition).addTo(this.map);
        }

        this.map.on("click", this._onMapClick.bind(this));

        setTimeout(() => {
            if (this.map) {
                this.map.invalidateSize();
            }
        }, 0);
    }

    destroyMap() {
        if (this.map) {
            this.map.remove();
            this.map = null;
            this.marker = null;
        }
    }

    _onMapClick(e) {
        const latlng = e.latlng;
        const lat = latlng.lat;
        const lng = latlng.lng;

        if (this.marker) {
            this.marker.setLatLng(latlng);
        } else {
            this.marker = L.marker(latlng).addTo(this.map);
        }

        this.props.record.update({
            map_latitude: lat,
            map_longitude: lng,
        });
    }

    onApplyCoordinatesClick() {
        const recordData = this.props.record.data || {};
        const lat = recordData.map_latitude;
        const lon = recordData.map_longitude;

        if (!lat || !lon) {
            console.warn("Map coordinates are empty. Please fill map_latitude and map_longitude first.");
            return;
        }

        if (!this.map || !window.L) {
            console.warn("Map is not initialized yet.");
            return;
        }

        const latlng = [lat, lon];

        this.map.setView(latlng, this.map.getZoom() || 13);

        if (this.marker) {
            this.marker.setLatLng(latlng);
        } else {
            this.marker = L.marker(latlng).addTo(this.map);
        }
    }
}

GeoLeafletMap.template = "GeoLeafletMapTemplate";

registry.category("fields").add("geo_leaflet_map_viewer", {
    component: GeoLeafletMap,
    supportedTypes: ["char"],
});