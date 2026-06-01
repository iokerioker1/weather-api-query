# 天气查询工具

## 项目简介
基于 Python 的命令行天气查询工具，通过 OpenWeatherMap API 获取实时天气数据。

## 技术栈
- Python 3
- Requests
- JSON
- OpenWeatherMap API

## 主要功能
- 输入城市名称查询天气
- 展示温度、湿度、气压、天气状况
- 包含异常处理（城市不存在 / 网络错误）

## 如何运行
1. 安装依赖
   pip install requests

2. 获取 API Key
   在 OpenWeatherMap 官网免费注册

3. 运行脚本
   python weather.py

## 项目结构
weather_project/
├── __init__.py
├── main.py
└── utils.py

## 备注
本地测试环境：Windows + PyCharm
