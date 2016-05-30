#!/usr/bin/python
# -*- coding: utf8 -*-

##### 임포트 시작 #####
# 인자 얻기
import sys
# csv 다루기
import csv

##### 임포트 끝 #####



##### 메인 시작 #####
def main():
	if( len(sys.argv) < 3 ):
		print '사용법: python score.py 입력파일 출력파일'
		sys.exit(0)

	print '받은 입력:', str(sys.argv[0]), str(sys.argv[1]), str(sys.argv[2])
	print str(sys.argv[1]), '에 있는 답안 결과를', str(sys.argv[2]), \
		'와 대조해 점수를 출력합니다.'
	
##### 메인 끝 #####




##### 스크립트 시작 #####
if __name__ == '__main__':
	main()
##### 스크립트 끝 #####
