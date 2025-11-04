import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)


class EmailSender:
    """邮件发送器"""

    def __init__(self, smtp_server: str, smtp_port: int,
                 sender_email: str, sender_password: str,
                 enable_ssl: bool = True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.enable_ssl = enable_ssl

    def create_alert_email(self, alerts: List[str], receiver: str) -> MIMEMultipart:
        """创建预警邮件"""
        message = MIMEMultipart()
        message['From'] = Header(f"天气预警系统 <{self.sender_email}>", 'utf-8')
        message['To'] = Header(receiver, 'utf-8')
        message['Subject'] = Header(f"天气预警通知 - {datetime.now().strftime('%Y-%m-%d %H:%M')}", 'utf-8')

        # HTML内容
        html_content = self._generate_html_content(alerts)
        message.attach(MimeText(html_content, 'html', 'utf-8'))

        return message

    def _generate_html_content(self, alerts: List[str]) -> str:
        """生成HTML邮件内容"""
        alert_items = "".join([f"<li style='color: red; margin: 10px 0;'>{alert}</li>" for alert in alerts])

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ color: #d63031; border-bottom: 2px solid #d63031; padding-bottom: 10px; }}
                .alert-list {{ background: #fff3cd; padding: 15px; border-radius: 5px; }}
                .footer {{ margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚨 天气预警通知</h1>
                <p>检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <div class="alert-list">
                <h3>预警信息 ({len(alerts)} 条):</h3>
                <ul>
                    {alert_items}
                </ul>
            </div>

            <div class="footer">
                <p><small>此邮件由天气预警系统自动发送，请勿回复</small></p>
            </div>
        </body>
        </html>
        """

    def send_email(self, receiver: str, message: MIMEMultipart) -> bool:
        """发送邮件"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.enable_ssl:
                    server.starttls()

                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.send_email, receiver, message.as_string())

            logger.info(f"成功发送邮件到 {receiver}")
            return True

        except Exception as e:
            logger.error(f"发送邮件失败: {e}")
            return False

    def send_alert(self, alerts: List[str], receiver: str) -> bool:
        """发送预警邮件"""
        if not alerts:
            logger.info("没有预警信息，跳过邮件发送")
            return True

        message = self.create_alert_email(alerts, receiver)
        return self.send_email(receiver, message)