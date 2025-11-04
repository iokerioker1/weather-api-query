import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class AlertManager:
    """预警管理器"""

    def __init__(self, config: Dict):
        self.temperature_high = float(config.get('temperature_high', 35))
        self.temperature_low = float(config.get('temperature_low', -5))
        self.rain_threshold = float(config.get('rain_threshold', 80))
        self.wind_threshold = float(config.get('wind_threshold', 15))
        self.humidity_threshold = float(config.get('humidity_threshold', 90))

    def check_weather_alerts(self, weather_data: Dict) -> List[str]:
        """检查天气预警条件"""
        alerts = []

        if not weather_data:
            return alerts

        city = weather_data['city']
        temp = weather_data['temperature']
        wind_speed = weather_data['wind_speed']
        rain = weather_data['rain_1h']
        humidity = weather_data['humidity']
        main_weather = weather_data['main_weather']
        description = weather_data['description']

        # 高温预警
        if temp > self.temperature_high:
            alerts.append(f"🌡️ {city} 高温预警: {temp}°C (阈值: {self.temperature_high}°C)")

        # 低温预警
        if temp < self.temperature_low:
            alerts.append(f"❄️ {city} 低温预警: {temp}°C (阈值: {self.temperature_low}°C)")

        # 大风预警
        if wind_speed > self.wind_threshold:
            alerts.append(f"💨 {city} 大风预警: {wind_speed} m/s (阈值: {self.wind_threshold} m/s)")

        # 降雨预警
        if rain > self.rain_threshold:
            alerts.append(f"🌧️ {city} 强降雨预警: {rain} mm (阈值: {self.rain_threshold} mm)")

        # 高湿预警
        if humidity > self.humidity_threshold:
            alerts.append(f"💧 {city} 高湿预警: {humidity}% (阈值: {self.humidity_threshold}%)")

        # 特殊天气预警
        severe_weather_keywords = ['雷暴', '暴雨', '大雪', '台风', '飓风', '冰雹']
        if any(keyword in description for keyword in severe_weather_keywords):
            alerts.append(f"⚠️ {city} 特殊天气预警: {description}")

        # 极端天气类型
        extreme_weather_types = ['Thunderstorm', 'Tornado', 'Hurricane']
        if main_weather in extreme_weather_types:
            alerts.append(f"🚨 {city} 极端天气预警: {main_weather}")

        if alerts:
            logger.info(f"{city} 触发 {len(alerts)} 条预警")

        return alerts

    def check_multiple_cities(self, weather_data_dict: Dict[str, Dict]) -> List[str]:
        """检查多个城市的预警"""
        all_alerts = []

        for city, weather_data in weather_data_dict.items():
            city_alerts = self.check_weather_alerts(weather_data)
            all_alerts.extend(city_alerts)

        return all_alerts