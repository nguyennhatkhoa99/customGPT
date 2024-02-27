from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable
from airflow.operators.python import get_current_context
import psycopg2
import logging
import pandas as pd
from ast import literal_eval
from gspread_pandas import Spread
from google.oauth2.credentials import Credentials

logger = logging.getLogger("airflow.task")
POSTGRES_CONNECTION = PostgresHook.get_connection('redmine_postgres')
CREDS_LIST = literal_eval(Variable.get('creds_list'))

default_params = {
"year": "2024",
"month":"02",
"spreadsheet": "1vEx8KMhLW1xWw3KgK3xmoSkNEoihR-jOtgjyGpLcgu0",
"sheet_name": "leave request"}


@dag(default_args={'owner': 'airflow', 'depends_on_past': False, 'start_date': days_ago(8)}, max_active_runs=1, catchup=False, params=default_params)
def export_leave_request():
    @task
    def get_setting_db():
        db_settings = {
            "host": POSTGRES_CONNECTION.host,
            "database": POSTGRES_CONNECTION.schema,
            "user": POSTGRES_CONNECTION.login,
            "password": POSTGRES_CONNECTION.password,
            "port": POSTGRES_CONNECTION.port
        }
        return db_settings
    @task
    def execute(db_settings: dict):
        context = get_current_context()
        dag_conf = context["dag_run"].conf
        month = dag_conf["month"]
        year = dag_conf["year"]
        sql = f"""
                SELECT 
                    user_id,
                    concat( ru.firstname, ' ', ru.lastname )  AS fullname,
                    lt.name as leave_type,
                    approved ,hours_per_day as number_of_days,
                    notes,
                    start_date as start_date_off,
                    end_date as end_date_off
                FROM dayoffs d
                    inner join users ru on d.user_id=ru.id
                    inner join leave_types lt on d.leave_type_id=lt.id
                WHERE
                    EXTRACT(YEAR FROM d.start_date) = {year} and EXTRACT(MONTH FROM d.start_date) = {month}
                """
        with psycopg2.connect(**db_settings) as conn:
            logger.info(f'Executing query: {sql}')
            df = pd.read_sql_query(sql, conn)
            logger.info(df.head())
            logger.info(df.info())
            return df
    @task
    def export_data_to_gsheet(df):
        creds = Credentials.from_authorized_user_info(CREDS_LIST[0])
        context = get_current_context()
        dag_conf = context["dag_run"].conf
        spreadsheet_url = dag_conf['spreadsheet']
        sheet_tab_name = dag_conf['sheet_name']
        target_spread = Spread(
            spread = spreadsheet_url,
            creds = creds,
            sheet= sheet_tab_name)
        
        sheet_rows, sheet_cols = target_spread.get_sheet_dims()
        logger.info(sheet_rows)
        logger.info(sheet_cols)
        target_spread.df_to_sheet(
                df, 
                index=False,
                headers=True,
                start='A1')
        df_list = df.values.tolist()
        req_rows = len(df_list)
        logger.info(len(df_list[0]))
        if req_rows:
            req_cols = len(df_list[0]) +  1
            logger.info((sheet_rows - req_rows - 1) * req_cols)
            if (sheet_rows - req_rows - 1) > 0:
                 target_spread.update_cells(
                    start=(req_rows, 1),
                    end=(sheet_rows, req_cols),
                    vals=["" for i in range(0, (sheet_rows - req_rows + 1) * req_cols)])

    setting = get_setting_db()
    data_frame = execute(setting)
    export_data_to_gsheet(data_frame)

run = export_leave_request()
