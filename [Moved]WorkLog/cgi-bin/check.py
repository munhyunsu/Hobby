#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import modules for CGI handling 
import cgi, cgitb
cgitb.enable()
import sqlite3
import time

# 유저 아이디 / 패스워드
form = cgi.FieldStorage() 
user_id = form.getvalue('id')
check_flag = None

connector = sqlite3.connect('userdatabase.sqlite')
cursor = connector.cursor()
cursor.execute('SELECT mac FROM user WHERE id=' + user_id)
mac = cursor.fetchone()[0]

if mac == None:
    check_flag = False

if check_flag == None:
    connector = sqlite3.connect('classscan.sqlite')
    cursor = connector.cursor()
    cursor.execute('SELECT unix_time, identifier FROM classscan '
                 + 'WHERE scanned_mac LIKE "%' + mac + '%" '
                 + 'ORDER BY unix_time ASC')
    log_set = cursor.fetchall()
    if log_set != None:
        check_flag = True

if check_flag == True:
    print("Content-type:text/html\r\n\r\n")
    print("<html>")
    print("<head>")
    print("    <title>DNLab 출석부</title>")
    print("</head>")
    print("<body>")
    print("    <h1>정보 확인 성공</h1>")
    print("    <h2>안녕하세요. {0} ({1})</h2>".format(user_id, mac))
    print("    <p>")
    print("      시간 장소<br>")
    for log in log_set:
        log_time = log[0]
        log_identifier = log[1]
        strtime = time.strftime('%Y.%m.%d %H:%M:%S', 
                                time.localtime(log_time))
        print("      {0} {1}<br>".format(strtime, log_identifier))
    print("    </p>")
    print("    <a href='/index.html'> Return to mainpage </a>")
    print("</body>")
    print("</html>")
else:
    print("Content-type:text/html\r\n\r\n")
    print("<html>")
    print("<head>")
    print("    <title>DNLab 출석부</title>")
    print("</head>")
    print("<body>")
    print("    <h1>정보 확인 실패</h1>")
    print("    <h2>등록되지 않은 학번이거나 학번을 잘못입력했습니다.</h2>")
    print("    <h3>{0}</h3>".format(user_id))
    print("    <a href='/index.html'> Return to mainpage </a>")
    print("</body>")
    print("</html>")
