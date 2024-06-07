import logging

import logging
from datetime import datetime
# 获取当前时间的字符串表示，用于构造带时间戳的文件名
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_name ='log/' +f'google_scholar_spider_{current_time}.log'
logging.basicConfig(
    level=logging.INFO     # 设置最低日志级别为INFO
)
def get_logger():
    # 1. 创建一个logger对象
    my_logger = logging.getLogger("first_logger")

    # 2. 定义handler
    my_handler = logging.FileHandler(log_file_name, mode='w', encoding='utf-8')

    # 3. 设置日志级别和Formatter
    my_handler.setLevel(logging.INFO)
    my_format = logging.Formatter("级别:%(levelname)s 时间:%(asctime)s 日志信息:%(message)s 行号:%(lineno)d")
    my_handler.setFormatter(my_format)

    # 4. 添加handler到logger
    my_logger.addHandler(my_handler)
    return my_logger

# 其他模块可以这样使用
# from your_module import get_logger
logger = get_logger()
logger.info("这是一个测试日志")

