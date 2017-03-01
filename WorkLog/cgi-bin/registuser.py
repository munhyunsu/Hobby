#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules for CGI handling 
import cgi, cgitb
cgitb.enable()
import sqlite3

# 유저 학번 / MAC 주소
form = cgi.FieldStorage() 
user_id = form.getvalue('id')
user_mac  = form.getvalue('mac')
user_mac = user_mac.upper()
regist_flag = None
try:
    connector = sqlite3.connect('userdatabase.sqlite')
    cursor = connector.cursor()
    cursor.executescript('''
            CREATE TABLE IF NOT EXISTS user
            ( id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            mac TEXT );
            ''')
    connector.commit()

    cursor.executescript('''
            UPDATE OR IGNORE user
            SET '''
            + 'id="' + user_id + '", '
            + 'mac="' + user_mac + '" '
            + '''WHERE '''
            + 'id="' + user_id + '";'
            + '''
            INSERT OR IGNORE INTO user
            (id, mac) VALUES ('''
            + '"' + user_id + '", '
            + '"' + user_mac + '");')
    connector.commit()
    regist_flag = True
except Exception as err:
    print(err)
    regist_flag = False

if regist_flag == True:
    print("Content-type:text/html\r\n\r\n")
    print("<html>")
    print("<head>")
    print("    <title>DNLab 출석부</title>")
    print("</head>")
    print("<body>")
    print("    <h1>MAC주소가 등록되었습니다.</h1>")
    print("    <h2>안녕하세요. {0} {1}</h2>".format(user_id, user_mac))
    print("    <a href='/index.html'>메인페이지로 가기</a>")
    print("</body>")
    print("</html>")
else:
    print("Content-type:text/html\r\n\r\n")
    print("<html>")
    print("<head>")
    print("    <title>DNLab 출석부</title>")
    print("</head>")
    print("<body>")
    print("    <h1>MAC주소 등록에 실패했습니다.</h1>")
    print("    <h1>개발자에게 알려주세요.</h1>")
    print("    <h2>입력된 정보: {0} {1}</h2>".format(user_id, user_mac))
    print("</body>")
    print("</html>")
