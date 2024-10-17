from database.db_handler import get_Transactions_Dataframe
from utils.income_outcome_area import income_outcome_area

df = get_Transactions_Dataframe()

income_outcome_area(df)