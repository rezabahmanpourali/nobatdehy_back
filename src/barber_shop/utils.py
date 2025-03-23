from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from typing import Dict, Optional

def get_address_from_coordinates(latitude: float, longitude: float) -> Optional[Dict[str, str]]:
    """
    تبدیل مختصات جغرافیایی به آدرس متنی با استفاده از OpenStreetMap
    """
    try:
        geolocator = Nominatim(user_agent="nobatdehy")
        location = geolocator.reverse((latitude, longitude), language='fa')
        
        if location and location.raw.get('address'):
            address_data = location.raw['address']
            return {
                'address': address_data.get('road', '') + ' ' + address_data.get('house_number', ''),
                'city': address_data.get('city', '') or address_data.get('town', '') or address_data.get('village', ''),
                'state': address_data.get('state', ''),
                'postal_code': address_data.get('postcode', ''),
                'country': address_data.get('country', '')
            }
        return None
    except GeocoderTimedOut:
        return None
    except Exception as e:
        print(f"خطا در دریافت آدرس: {str(e)}")
        return None 