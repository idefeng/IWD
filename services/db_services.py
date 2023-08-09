import sqlite3 as sl


def check(db_name, table_name):
    conn = sl.connect("IWD.db")
    cur = conn.cursor()
    sql = '''
        SELECT tbl_name FROM sqlite_master WHERE type='table'
    '''
    cur.execute(sql)
    values = cur.fetchall()
    tables = []
    for v in values:
        tables.append(v[0])
    if table_name not in tables:
        return False
    else:
        return True


if __name__ == "__main__":
    conn = sl.connect("IWD.db")
    cur = conn.cursor()
    if not check("IWD.db", "download"):
        sql = '''
            CREATE TABLE download();
        '''
        cur.execute(sql)
