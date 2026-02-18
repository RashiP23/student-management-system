# import cx_Oracle

# def get_connection():
#     """
#     Creates and returns Oracle DB connection
#     """
#     connection = cx_Oracle.connect(
#         user="system",
#         password="your_password",
#         dsn="localhost/XE"   # change if needed
#     )
#     return connection
# import oracledb

# def get_connection():
#     return oracledb.connect(
#         user="system",
#         password="system",
#         dsn="C:\Users\rashi\Desktop\instantclient-basic-windows.x64-23.26.0.0.0"
#     )
import oracledb

# Enable Thick mode (required for Oracle 11g)
# oracledb.init_oracle_client(
#     lib_dir=r"C:\oracle\instantclient_23"
# )

# def get_connection():
#     return oracledb.connect(
#         user="system",
#         password="system",   # use your actual Oracle password
#         dsn="localhost/XE"
#     )
# import oracledb

# def get_connection():
#     return oracledb.connect(
#         user="system",
#         password="system",   # your Oracle password
#         dsn="localhost/XE"
#     )
import oracledb

# FORCE thick mode (required for Oracle 11g)
oracledb.init_oracle_client()

def get_connection():
    return oracledb.connect(
        user="system",
        password="system",   # your Oracle DB password
        dsn="localhost/XE"
    )
