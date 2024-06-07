from urllib.parse import quote_plus
from sqlalchemy import create_engine
from dotenv import find_dotenv, load_dotenv
import os
from log.logger import get_logger
logger = get_logger()
# Load environment variables from .env file
env_dist = os.environ
load_dotenv(find_dotenv('.env'))

username= env_dist.get('dbusername')
password= env_dist.get('dbpassword')
dbHost= env_dist.get('dbHost')
dbPort=env_dist.get('dbPort')
dbName = env_dist.get('dbName')

db_url = f'mysql://{username}:{quote_plus(password)}@{dbHost}:{dbPort}/{dbName}?charset=utf8'
# 创建数据库引擎
engine = create_engine(db_url)

def save_to_mysql(data):
    # 将DataFrame写入MySQL数据库的表中，如果表不存在，SQLAlchemy默认会尝试创建它
    data.to_sql(name='chemical weapon defence', con=engine, if_exists='append', index=False)
    logger.info("Data successfully stored into MySQL database.")