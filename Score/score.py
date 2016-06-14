#/usr/bin/python
# -*- coding: utf8 -*-

##### 임포트 시작 #####
# 인자 얻기
import sys
# csv 다루기
import csv

##### 임포트 끝 #####



##### 메인 시작 #####
def main():
    # 인자 확인
    # 인자가 모자랄 경우 강제 종료
    if( len(sys.argv) < 3 ):
        print '사용법: python score.py 학생답안 선생님답안\n'
        sys.exit(0)

    # 입력 인자 출력 for 사용자편의 
    print '받은 입력:', str(sys.argv[0]), str(sys.argv[1]), str(sys.argv[2]), '\n'

    # 입력 인자 변수에 할당
    student = str(sys.argv[1])
    teacher = str(sys.argv[2])
    result = str(sys.argv[1]).split('.')[0] + str('_학생별점수.csv')
    print student, '에 있는 답안 결과를', teacher, '와 대조해 점수를 출력합니다.\n'

    # 답안 파일 읽어오기
    teacher_file = open(teacher, 'r')
    teacher_csv = csv.reader(teacher_file, delimiter = ',', quotechar = '"')
    answer_list = list()
    for (answer_number, answer_score) in teacher_csv:
        answer_list.append( (int(answer_number), int(answer_score)) )

    # 결과 파일 만들기
    result_file = open(result, 'w')
    result_csv = csv.writer(result_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)

    # 학생 파일 읽어오기
    student_file = open(student, 'r')
    student_csv = csv.reader(student_file, delimiter = ',', quotechar = '"')

    # 학생 파일 순회
    for rows in student_csv:
        # 학생 정보 임시 저장
        s_grade = rows[0]
        s_class = rows[1]
        s_number = rows[2]
        # 답 리스트로 저장
        s_answer = rows[3:len(rows)]
        # 점수는 0으로 초기화
        s_score = 0
        
        # 답 체크
        for index in range(0, len(s_answer)):
            # 답을 입력 안 했을 경우가 존재 예외처리 해야 함
            # 이중 if문보다 나을 것으로 판단(가독성)
            try:
                if( (answer_list[index])[0] == int(s_answer[index]) ):
                    s_score = s_score + (answer_list[index])[1]
            except ValueError:
                pass
        
        result_csv.writerow([s_grade, s_class, s_number, s_score])

    ### 추가
    result_answer_rate = str(sys.argv[1]).split('.')[0] + str('_문항별정답률.csv')
    answer_rate_file = open(result_answer_rate, 'w')
    answer_rate_csv = csv.writer(answer_rate_file, delimiter = ',' , quotechar = '"', quoting = csv.QUOTE_MINIMAL)

    # 답안 수 초기화
    teacher_file.seek(0)
    answer_rate = list()
    for rows in teacher_csv:
        answer_rate.append(dict())

    # 문항별 답안 수 집계
    student_file.seek(0)
    for rows in student_csv:
        student_answer = rows[3:len(rows)]
        for index in range(0, len(student_answer)):
            try:
                dict_key = int(student_answer[index])
                (answer_rate[index])[dict_key] = (answer_rate[index]).get(dict_key, 0) + 1
            except ValueError:
                dict_key = int(0)
                (answer_rate[index])[dict_key] = (answer_rate[index]).get(dict_key, 0) + 1
                
    index = 0
    for answer in answer_rate:
        answer_0 = float(answer.get(0, 0)) / float(sum(answer.values()))
        answer_1 = float(answer.get(1, 0)) / float(sum(answer.values()))
        answer_2 = float(answer.get(2, 0)) / float(sum(answer.values()))
        answer_3 = float(answer.get(3, 0)) / float(sum(answer.values()))
        answer_4 = float(answer.get(4, 0)) / float(sum(answer.values()))
        answer_5 = float(answer.get(5, 0)) / float(sum(answer.values()))

        answer_rate_csv.writerow([(answer_list[index])[0], answer_0, answer_1, answer_2, answer_3, answer_4, answer_5])
        index = index + 1


    ### 추가 끝







    # 결과 출력
    print '계산 완료!'
    print '출력 결과는', result, '입니다\n'
    # 사사문구
    print '추가 보완 사항은 개인적으로 연락주세용!\n'

    # 파일 닫기
    teacher_file.close()
    result_file.close()
    student_file.close()
    answer_rate_file.close()
##### 메인 끝 #####




##### 스크립트 시작 #####
if __name__ == '__main__':
    main()
##### 스크립트 끝 #####
