from tests_collection import TESTS_COLLECTION

from utils.testing_system import run_many

from utils.logger import set_log_lvl, LogFlags
set_log_lvl(LogFlags.NO)


df_path = 'res.csv'
run_many(TESTS_COLLECTION, df_path, csv_mode='w')
