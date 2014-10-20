DB_USER = "ormiret_tinfoil"
DB_PASS = "workforceashamed5__)9"
DB_NAME = DB_USER
DB_SERVER = "localhost"

DB_CONN = "mysql+mysqldb://{user}:{passwd}@{server}/{db}?charset=utf8".format(
    user=DB_USER,
    passwd=DB_PASS,
    server=DB_SERVER,
    db=DB_NAME)
