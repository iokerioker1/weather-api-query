import logging
import logging.config
import configparser
from typing import List, Dict
from datetime import datetime

from .weather_api import WeatherAPI
from .email_sender import EmailSender
from .alert_manager import AlertManager


class WeatherMonitor:
    """天气监控系统核心类"""

    def __init__(self, config_file: str = 'config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')

        self._setup_logging()
        self.logger = logging.getLogger(__name__)

        # 初始化组件
        self.weather_api = self._init_weather_api()
        self.email_sender = self._init_email_sender()
        self.alert_manager = self._init_alert_manager()

        self.cities = self._get_cities()

    def _setup_logging(self):
        """配置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/weather_monitor.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def _init_weather_api(self) -> WeatherAPI:
        """初始化天气API客户端"""
        api_key = self.config['WEATHER']['api_key']
        base_url = self.config['WEATHER'].get('base_url', 'http://api.openweathermap.org/data/2.5/weather')
        return WeatherAPI(api_key, base_url)

    def _init_email_sender(self) -> EmailSender:
        """初始化邮件发送器"""
        email_config = self.config['EMAIL']
        return EmailSender(
            smtp_server=email_config['smtp_server'],
            smtp_port=int(email_config['smtp_port']),
            sender_email=email_config['sender_email'],
            sender_password=email_config['sender_password'],
            enable_ssl=email_config.getboolean('enable_ssl', True)
        )

    def _init_alert_manager(self) -> AlertManager:
        """初始化预警管理器"""
        alert_config = dict(self.config['ALERT'])
        return AlertManager(alert_config)

    def _get_cities(self) -> List[str]:
        """获取监控城市列表"""
        cities_str = self.config['WEATHER']['cities']
        return [city.strip() for city in cities_str.split(',')]

    def run_monitoring(self) -> Dict:
        """执行一次完整的监控任务"""
        self.logger.info(f"开始天气监控，城市: {', '.join(self.cities)}")

        # 获取天气数据
        weather_data = self.weather_api.get_multiple_cities_weather(self.cities)

        # 检查预警
        alerts = self.alert_manager.check_multiple_cities(weather_data)

        # 发送预警邮件
        if alerts:
            receiver = self.config['EMAIL']['receiver_email']
            success = self.email_sender.send_alert(alerts, receiver)

            if success:
                self.logger.info(f"成功发送 {len(alerts)} 条预警信息")
            else:
                self.logger.error("发送预警邮件失败")
        else:
            self.logger.info("所有城市天气正常，无需发送预警")

        # 返回监控结果
        return {
            'timestamp': datetime.now(),
            'cities_monitored': len(self.cities),
            'cities_success': len(weather_data),
            'alerts_triggered': len(alerts),
            'alerts': alerts,
            'weather_data': weather_data
        }

    def get_status(self) -> Dict:
        """获取系统状态"""
        return {
            'cities': self.cities,
            'alert_rules': {
                'temperature_high': self.alert_manager.temperature_high,
                'temperature_low': self.alert_manager.temperature_low,
                'rain_threshold': self.alert_manager.rain_threshold,
                'wind_threshold': self.alert_manager.wind_threshold
            },
            'email_config': {
                'sender': self.email_sender.sender_email,
                'receiver': self.config['EMAIL']['receiver_email']
            }
        }