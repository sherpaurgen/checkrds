import sqlite3
import logging

def create_diskusage_table(db_file):
    try:
        conn=sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS disk_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                DBInstanceIdentifier TEXT,
                                Engine TEXT,
                                DiskUsage REAL,
                                region_name TEXT,
                                updatedat CURRENT_TIMESTAMP
                            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, create_diskusage_table: " + str(e))

def create_cpuusage_table(db_file):
    try:
        conn=sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cpu_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                DBInstanceIdentifier TEXT,
                                Engine TEXT,
                                CpuUsage REAL,
                                region_name TEXT,
                                updatedat CURRENT_TIMESTAMP
                            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, create_cpuusage_table: " + str(e))


def create_memusage_table(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS mem_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                DBInstanceIdentifier TEXT,
                                Engine TEXT,
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
            "INSERT INTO cpu_usage (DBInstanceIdentifier,Engine,CpuUsage,region_name) VALUES (?, ?, ?, ?)",
            (data["DBInstanceIdentifier"], data["Engine"], data["CpuUsage"], data["region_name"]))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.warning("DB Error, insert_cpuusage_data: " + str(e))
