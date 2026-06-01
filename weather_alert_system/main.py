"""天气预警系统主入口"""

import sys
import time
import schedule
from weather_monitor.core import WeatherMonitor


def main():
    """主函数"""
    try:
        monitor = WeatherMonitor('config.ini')

        print("天气预警系统")
        print("=" * 30)

        # 显示系统状态
        status = monitor.get_status()
        print(f"监控城市: {', '.join(status['cities'])}")
        print(f"高温阈值: {status['alert_rules']['temperature_high']}°C")
        print(f"低温阈值: {status['alert_rules']['temperature_low']}°C")
        print()

        # 选择运行模式
        print("请选择运行模式:")
        print("1. 单次执行")
        print("2. 定时执行（每30分钟）")
        print("3. 退出")

        choice = input("请输入选择 (1/2/3): ").strip()

        if choice == "1":
            print("\n开始单次监控...")
            result = monitor.run_monitoring()
            print(f"\n监控完成: {result['cities_success']}/{result['cities_monitored']} 城市成功")
            print(f"触发预警: {result['alerts_triggered']} 条")

        elif choice == "2":
            print("\n启动定时监控，每30分钟执行一次...")
            print("按 Ctrl+C 停止")

            # 立即执行一次
            monitor.run_monitoring()

            # 设置定时任务
            schedule.every(30).minutes.do(monitor.run_monitoring)

            while True:
                schedule.run_pending()
                time.sleep(1)

        elif choice == "3":
            print("退出系统")
            sys.exit(0)
        else:
            print("无效选择，默认执行单次模式")
            monitor.run_monitoring()

    except KeyboardInterrupt:
        print("\n\n用户中断，退出系统")
    except Exception as e:
        print(f"系统运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
