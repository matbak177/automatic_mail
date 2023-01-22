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

class SendMail():
    
    def __init__(self,sender,receiver,subject,query,length):
        self.sender=sender
        self.receiver=receiver
        self.subject=subject
        # self.body=body
        self.query=query
        self.length=length
        
    @staticmethod    
    def MySQLConnect():
        mydb = mysql.connector.connect(
            user='mateusz'
            ,password=os.environ["mysql_password"]
            ,host='localhost'
            ,database='python'
        )
    
        return mydb
    
    def read_data(self):
        df = pd.read_sql_query(self.query,self.MySQLConnect())
        return df
    
    def table(self):
        tabela=""
    
        self.liczba = len(self.read_data())
        
        if self.liczba <self.length:
            tabela = """
                    <html>
                    <p>Below you will find your users with their results.<br>
                    <p>{tabela}</p>
                    </hrml>
                    """.format(tabela=build_table(self.read_data(),color='blue_light',font_size='small',font_family='Arial'))
    
        return tabela

    def send_notification(self):
        body="""
            <html>
            <p>Hello,
            <br>I would like to inform you about your users and theirs results.
            <br>I highly recommend you to take look at it.</p>
            <p>{tabela}</p>
            <p>In case of any question feel free to concact to me.</p>
            """.format(tabela=self.table())
        
        server=smtplib.SMTP_SSL('smtp.gmail.com',465)
        message =MIMEMultipart()
        message['Subject']=self.subject
        message['From']=self.sender
        message['To']=self.receiver
        message.attach(MIMEText(body,'html'))
        server.login(self.sender,os.environ["mail_password"])
        
        if self.liczba>self.length:
            attachment=MIMEApplication(self.read_data().to_csv())
            attachment['Content-Disposition']='attachment;filename="{}"'.format("'users.csv")
            message.attach(attachment)
        
        try:
            server.sendmail(self.sender,self.receiver,message.as_string())
            print('udalo sie')
        except smtplib.SMTPException as e:
            print(str(e))
        server.quit()
            
SendMail('matbak177@gmail.com','mat177@onet.eu','List of users','Select * from mail',5).send_notification()
