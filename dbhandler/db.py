import sqlite3
import logging

def create_diskfree_table(db_file):
    try:
        conn=sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS disk_free (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                DBInstanceIdentifier TEXT,
                                Engine TEXT,
                                DBInstanceStatus TEXT,
                                disk_free REAL,
                                region_name TEXT,
                                updatedat CURRENT_TIMESTAMP
                            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, create_diskusage_table: " + str(e))

def insert_diskfree_data(db_file,data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO disk_free (DBInstanceIdentifier,Engine,DBInstanceStatus,disk_free,region_name) VALUES (?, ?,?, ?, ?)",
            (data["DBInstanceIdentifier"], data["Engine"],data["DBInstanceStatus"], data["FreeStorageSpace"], data["region_name"]))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, insert_diskfree_data: " + str(e))


def create_cpuusage_table(db_file):
    try:
        conn=sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cpu_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                DBInstanceIdentifier TEXT,
                                Engine TEXT,
                                DBInstanceStatus TEXT,
                                CpuUsage REAL,
                                region_name TEXT,
                                updatedat CURRENT_TIMESTAMP
                            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, create_cpuusage_table: " + str(e))

def create_diskqueuedepth_table(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS diskqueuedepth (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                DBInstanceIdentifier TEXT,
                                Engine TEXT,
                                DBInstanceStatus TEXT,
                                diskqueuedepth REAL,
                                region_name TEXT,
                                updatedat CURRENT_TIMESTAMP
                            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, create_diskqueuedepth_table: " + str(e))

def create_memfree_table(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS mem_free (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                DBInstanceIdentifier TEXT,
                                Engine TEXT,
                                DBInstanceStatus TEXT,
                                MemUsage REAL,
                                region_name TEXT,
                                updatedat CURRENT_TIMESTAMP
                            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, create_memusage_table: " + str(e))

def insert_cpuusage_data(db_file,data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO cpu_usage (DBInstanceIdentifier,Engine,DBInstanceStatus,CpuUsage,region_name) VALUES (?,?, ?, ?, ?)",
            (data["DBInstanceIdentifier"], data["Engine"],data["DBInstanceStatus"], data["cpu_usage"], data["region_name"]))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, insert_cpuusage_data: " + str(e))

def insert_diskqueuedepth_data(db_file,data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO diskqueuedepth (DBInstanceIdentifier,Engine,DBInstanceStatus,diskqueuedepth,region_name) VALUES (?,?, ?, ?, ?)",
            (data["DBInstanceIdentifier"], data["Engine"],data["DBInstanceStatus"], data["DiskQueueDepth"], data["region_name"]))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, insert_diskqueuedepth_data: " + str(e))

def insert_memfree_data(db_file,data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO mem_free (DBInstanceIdentifier,Engine,DBInstanceStatus,MemUsage,region_name) VALUES (?,?, ?, ?, ?)",
            (data["DBInstanceIdentifier"], data["Engine"],data["DBInstanceStatus"], data["memfreeable"], data["region_name"]))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, insert_memFreeable_data: " + str(e))

def create_elbresponsetime_table(db_file):
    try:
        conn=sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS elbresponsetime (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                LoadBalancerName TEXT,
                                DNSName TEXT,
                                avg_response_time REAL,
                                region_name TEXT,
                                elbState TEXT,
                                updatedat CURRENT_TIMESTAMP
                            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, create_elbresponsetime_table: " + str(e))

def create_elbtargetgroup_table(db_file):
    try:
        conn=sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS elbtargetgroup (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                LoadBalancerName TEXT,
                                targetgroup TEXT,
                                region_name TEXT,
                                alb_arn TEXT,
                                elbState TEXT,
                                unhealthycount REAL,
                                updatedat CURRENT_TIMESTAMP
                            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, create_elbtargetgroup_table: " + str(e))

def insert_elbtargetgroup_data(db_file,data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO elbtargetgroup (LoadBalancerName,targetgroup,region_name,alb_arn,elbState,unhealthycount) VALUES (?, ?, ?, ?,?,? )",
            (data["LoadBalancerName"], data["tgtarn"], data["region_name"], data["alb_arn"],data["State"],data["unhealthycount"]))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, insert_elbtargetgroup_data: " + str(e))

def insert_elbresponsetime_data(db_file,data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO elbresponsetime (LoadBalancerName,DNSName,avg_response_time,region_name,elbState) VALUES (?, ?, ?, ?, ?)",
            (data["LoadBalancerName"], data["DNSName"], data["avg_response_time"], data["region_name"],data["State"]))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, insert_elbresponsetime_data: " + str(e))

def truncate_tables(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    table_names = ['mem_free','disk_free','cpu_usage','diskqueuedepth','elbresponsetime','elbtargetgroup']
    for t in table_names:
        cursor.execute(f"DELETE FROM {t}")
    conn.commit()
    cursor.close()
    conn.close()

