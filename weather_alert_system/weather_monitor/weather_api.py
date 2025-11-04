import requests
import time
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class WeatherAPI:
    """天气API客户端"""

    def __init__(self, api_key: str, base_url: str = "http://api.openweathermap.org/data/2.5/weather"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()

    def get_weather(self, city: str, units: str = 'metric', language: str = 'zh_cn') -> Optional[Dict]:
        """获取城市天气数据"""
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units,
                'lang': language
            }

            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # 解析响应数据
            weather_info = {
                'city': city,
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'main_weather': data['weather'][0]['main'],
                'wind_speed': data['wind']['speed'],
                'wind_degree': data['wind'].get('deg', 0),
                'rain_1h': data.get('rain', {}).get('1h', 0),
                'snow_1h': data.get('snow', {}).get('1h', 0),
                'visibility': data.get('visibility', 0),
                'cloudiness': data['clouds']['all'],
                'sunrise': data['sys']['sunrise'],
                'sunset': data['sys']['sunset'],
                'country': data['sys']['country']
            }

            logger.info(f"成功获取 {city} 天气数据")
            return weather_info

        except requests.exceptions.RequestException as e:
            logger.error(f"获取 {city} 天气数据失败: {e}")
            return None
        except KeyError as e:
            logger.error(f"解析 {city} 天气数据失败，缺少字段: {e}")
            return None

    def get_multiple_cities_weather(self, cities: list, delay: float = 1.0) -> Dict[str, Dict]:
        """获取多个城市天气数据"""
        results = {}

        for city in cities:
            weather_data = self.get_weather(city)
            if weather_data:
                results[city] = weather_data
            time.sleep(delay)  # 避免API限制

        return results