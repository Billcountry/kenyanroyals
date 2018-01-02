import smtplib
import os
import random
import hashlib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from validate_email import validate_email
import sqlalchemy
from sqlalchemy import engine
from sqlalchemy.sql import schema, text
import pendulum


class status_code:
    unauthorized = 401
    forbidden = 403
    method_not_allowed = 405
    invalid_data = 433
    not_found = 404
    bad_request = 400
    success = 200
    system_error = 500
    not_implemented = 501
    redirect = 302


def log_error(title, data):
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        file = open(path + "/../logs/errors.md", "a+")
        file.write(">### "+title+"\n")
        file.write("*"+str(datetime.now())+"*\n")
        file.write("```\n"+data+"\n```\n\n")
        file.close()
        return True
    except IOError as e:
        print(str(e))
        return False


def api_return(success, message, status):
    return {
        "success": success,
        "message": message
    }, status


def sha256(text: str):
    hash_object = hashlib.sha256(text.encode())
    return hash_object.hexdigest()


def db_connect():
    try:
        url = os.environ.get("DATABASE_URL", "ALTERNATIVE_URL_GOES_HERE_PROBABLY_YOUR_LOCAL_TEST_DB")
        db_conn: engine = sqlalchemy.create_engine(url)
        db_meta: schema = sqlalchemy.MetaData(bind=db_conn, reflect=True)
    except Exception as e:
        db_conn = None
        db_meta = None
        log_error("Error connecting to database", str(e))
    return db_conn, db_meta


def db_insert(table: str, data: list):
    con, meta = db_connect()
    try:
        if con is not None:
            con.execute(meta.tables[table].insert(), data)
            return True
        else:
            return False
    except Exception as e:
        log_error("Error inserting data: ", str(e))
        return False


def db_execute_query(query, params={}):
    if params is None:
        params = {}
    con, meta = db_connect()
    try:
        if con is not None:
            stmt = text(query)
            stmt = stmt.bindparams(**params)
            return con.execute(stmt)
    except Exception as e:
        log_error("Error executing query: ", str(e))
    return None


def send_email(recipient: str, recipient_name: str, subject: str, template: str, template_values: dict,
               text_message="Please use a client that can read HTML email"):
    success = False
    status = 500
    try:
        if validate_email(recipient, verify=True):
            smtp = smtplib.SMTP("smtp.gmail.com", 587)  # initialize smtp class
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            message = template
            for key in list(template_values):
                message = message.replace(str(key), (template_values[key]))
            smtp.login("deliverymashinani@gmail.com", "RVxgKpTUktOVYG2L")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = 'From: DeMashina <accounts@demashina.com>'
            msg['To'] = recipient_name + ' <' + recipient + '>'
            plain = MIMEText(text_message, "plain")
            html = MIMEText(message, "html")
            msg.attach(plain)
            msg.attach(html)
            smtp.sendmail("deliverymashinani@gmail.com", recipient, msg.as_string())
            smtp.close()
            success = True
            message = "Your message was sent successfully."
        else:
            message = "Invalid or email does not exist"
        status = status_code.success
    except smtplib.SMTPException as e:
        message = "Error: Unable to send email: \n" + str(e)
    except (ConnectionRefusedError, ConnectionResetError, ConnectionResetError, ConnectionError) as e:
        message = "Connection error: Email not sent: \n"+str(e)
    except Exception as e:
        message = "Server Error: An error occurred: \n"+str(e)
    return {
        "success": success,
        "message": message,
        "status": status
    }


def random_string(size,
                  characters: str = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*()?"):
    return "".join(random.sample(characters, size))


def validate_phone(phone):
    phone = phone.replace("+", "")
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")
    if phone.isnumeric() and (
            (len(phone) == 9 and phone[0] == "7") or
            (len(phone) == 10 and phone[0:2] == "07") or
            (len(phone) == 12 and phone[0:4] == "2547")
    ) and (
            (0 <= int(phone[-8] + phone[-7]) < 40) or
            (60 <= int(phone[-8] + phone[-7]) < 100)
    ):
        return True,
    else:
        return False


def human_date(timestamp=datetime.now().timestamp(), date_only=False, time_ago=False, hours=0, minutes=0,
               sec=0, months=0, years=0, days=0):
    date = pendulum.from_timestamp(timestamp)
    date = date.add(years=years, months=months, weeks=0, days=days, hours=hours, minutes=minutes, seconds=sec)
    if date_only:
        return date.format('DD-MMM-YYYY', formatter='alternative')
    else:
        if time_ago:
            return date.diff_for_humans()
    return date.format('DD-MMM-YYYY HH:mm:ss', formatter='alternative')



def py_jax(url, method, data, headers):
    pass

