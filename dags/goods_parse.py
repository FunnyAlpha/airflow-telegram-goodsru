# 'fashionsearch_dag.py' in Airflow dag folder
import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
'owner': 'msolovev',
'depends_on_past': False,
'start_date': days_ago(1),
'retries': 1,
'retry_delay': timedelta(minutes=10),
# 'queue': 'bash_queue',
# 'pool': 'backfill',
# 'priority_weight': 10,
# 'end_date': datetime(2016, 1, 1),
}
dag = DAG(dag_id='parse_goods', default_args=default_args, schedule_interval=timedelta(days=1))
# This task deletes all json files which are generated in previous scraping sessions
t1 = BashOperator(
task_id='run_spider_goods',
bash_command='/parse_goods/scrapAmazon/scrapAmazon/spiders/start_goods_spider.sh',
dag=dag)

t2 = BashOperator(
task_id='telegram_send_report',
bash_command='/telegram/telegram.sh',
dag=dag)

# set up dependecies
t1 >> t2