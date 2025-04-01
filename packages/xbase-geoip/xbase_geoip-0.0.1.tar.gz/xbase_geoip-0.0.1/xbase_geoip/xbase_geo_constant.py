import os

current_dir = os.path.dirname(__file__)
assets_dir = "xbase_geoip_assets"
parse_js_path = os.path.join(current_dir, '..', assets_dir, 'arkimeparse.js')
geo_path_city = os.path.join(current_dir, '..', assets_dir, 'GeoLite2-City.mmdb')
geo_path_country = os.path.join(current_dir, '..', assets_dir, 'GeoLite2-Country.mmdb')
