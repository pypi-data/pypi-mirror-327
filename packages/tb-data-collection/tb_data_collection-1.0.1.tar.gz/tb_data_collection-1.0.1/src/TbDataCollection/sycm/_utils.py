import json
import re


def parse__localstorage_data(content: str):
    """解析格式化 localStorage 数据"""

    _data = re.sub(r'^\d+\|', '', content.strip('"').replace('\\', ''))
    data_json: dict = json.loads(_data)
    value: dict = data_json.get('value')

    return value.get('_d')
