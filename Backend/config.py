from sqlalchemy import URL

DATABASE_URL = URL.create(
    "mysql+pymysql",
    username = 'sakthi',
    password = 'Strong@$@Kth!@138540',
    host = 'localhost',
    database = 'value_addition_db'
)
