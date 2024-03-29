import smtplib, ssl
from email.message import EmailMessage
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from email.mime.application import MIMEApplication
from pretty_html_table import build_table
import mysql.connector
import pymysql
import os


password = os.environ["mysql_password"]
password_mail=os.environ["mail_password"]

mydb = mysql.connector.connect(
      user='mateusz'
    , password=password
    , host='localhost'
    , database='python'
)

# jeden sposob pobierania danych z mysql
receiver_query = mydb.cursor()
receiver_query.execute("Select distinct email,imie as email from mail")
receiver_query = receiver_query.fetchall()
receiver = pd.DataFrame(receiver_query)
receivers = receiver.values.tolist()


def send_mail():
    for i in receivers:

        # my_cursor = mydb.cursor()
        # my_cursor.execute("SELECT * FROM mail where imie ='{}'".format(i[1]))
        # myresult = my_cursor.fetchall()
        # df=pd.DataFrame(myresult)

        # drugi sposob pobierania - ten zawierania nazwy kolumn
        query = "Select * from mail where imie ='{}'".format(i[1])

        df = pd.read_sql_query(query, mydb)

        tabela = ""

        liczba = len(df)

        if liczba <= 3:
            tabela = """
                    <html>
                    <p>Below you will find your users with their results.<br>
                    <p>{tabela}</p>
                    </hrml>
                    """.format(tabela=build_table(df, color='blue_light', font_size='small', font_family='Arial'))

        body = """
            <html>
            <p>Hello {},
            <br>I would like to inform you about your users and theirs results.
            <br>I highly recommend you to take look at it.</p>
            <p>{tabela}</p>
            <p>In case of any question feel free to concact to me.</p>
            """.format(i[1], tabela=tabela)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        message = MIMEMultipart()
        message['Subject'] = 'List of users'
        message['From'] = 'Analyst - Mateusz'
        message['To'] = i[0]
        message.attach(MIMEText(body, 'html'))
        server.login('matbak177@gmail.com', password_mail)

        if liczba > 3:
            attachment = MIMEApplication(df.to_csv())
            attachment['Content-Disposition'] = 'attachment;filename="{}"'.format("'users.csv")
            message.attach(attachment)

        try:
            server.sendmail('matbak177@gmail.com', i[0], message.as_string())
            print('udalo sie')
        except smtplib.SMTPException as e:
            print(str(e))
        server.quit()

send_mail()