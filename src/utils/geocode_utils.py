# src/utils/geocode_utils.py

import os
from typing import List, Dict

import overpy

# Try to import googlemaps if you have a key
GMAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
if GMAPS_API_KEY:
    import googlemaps
    gmaps = googlemaps.Client(key=GMAPS_API_KEY)
else:
    gmaps = None  # signal “no Google client”

osm_api = overpy.Overpass()

def _find_with_gmaps(
    lat: float, lng: float, radius_m: int, keyword: str
) -> List[Dict]:
    places = gmaps.places_nearby(
        location=(lat, lng), radius=radius_m, keyword=keyword
    ).get("results", [])
    places.sort(
        key=lambda x: (x.get("rating", 0), x.get("user_ratings_total", 0)),
        reverse=True,
    )
    return places

def _find_with_osm(lat: float, lng: float, radius_m: int) -> List[Dict]:
    query = f"""
    (
      node["amenity"="clinic"]["healthcare:speciality"="allergist"](around:{radius_m},{lat},{lng});
      node["healthcare"="doctor"]["speciality"="allergist"](around:{radius_m},{lat},{lng});
    );
    out center tags;
    """
    res = osm_api.query(query)
    results = []
    for node in res.nodes:
        results.append({
            "name": node.tags.get("name", "Unknown"),
            "lat": node.lat,
            "lng": node.lon,
            "tags": node.tags
        })
    return results

def find_allergists(
    lat: float,
    lng: float,
    radius_m: int = 5000,
    keyword: str = "allergist"
) -> List[Dict]:
    """
    Try Google Maps if available; otherwise fall back to OSM.
    Returns up to 10 best-rated places.
    """
    # 1) Google Maps (only if we have a client)
    if gmaps:
        try:
            g_res = _find_with_gmaps(lat, lng, radius_m, keyword)
            if g_res:
                return g_res[:10]
        except Exception:
            pass  # any Google error → fallback

    # 2) Overpass (OSM)
    o_res = _find_with_osm(lat, lng, radius_m)
    return o_res[:10]
