#/usr/bin/python
# -*- coding: utf8 -*-


import sys # 인자 얻기
import csv # csv 다루기


def main():
    """
    메인 메소드
    """
    if( len(sys.argv) < 3 ): # 인자를 확인하고, 모자랄 경우 강제 종료
        print '사용법: python score.py 학생답안 선생님답안\n'
        sys.exit(0)

    print '받은 입력:', str(sys.argv[0]), \
            str(sys.argv[1]), str(sys.argv[2]), # 사용자 편의를 위해 
                                                # 입력 인자 출력

    student_input = str(sys.argv[1]) # 학생 답안
    teacher_input = str(sys.argv[2]) # 선생님 답안
    # 사용자 편의를 위해 진행 사항 출력
    print student_input, '에 있는 답안 결과를', \
            teacher_input, '와 대조해 점수를 출력합니다.\n' 

    teacher_file = open(teacher_input, 'r') # 답안 파일 읽어와 리스트에 저장
    teacher_list = list(csv.reader(teacher_file, 
            delimiter = ',', quotechar = '"'))
    teacher_file.close() # 선생님 답안 닫기

    answer_list = dict() # 선생님 답안을 dict() 형식으로 저장
    for (problem_number, answer_number_list, answer_score) in teacher_list:
        answer_list[int(problem_number)] = ( # 문제 번호
                set(), # 답은 OR가 가능
                int(answer_score) # 점수
                )
        for answer_number in (answer_number_list.strip()).split(' '):
            ((answer_list[int(problem_number)])[0]).add(int(answer_number))
    print answer_list

    student_file = open(student_input, 'r') # 학생 답안 불러오기
    student_list = list(csv.reader(student_file, 
            delimiter = ',', quotechar = '"')) # 학생 답안 리스트
    student_file.close() # 학생 답안 닫기

    student_score_file_name = '학생별점수.csv' # 결과 파일 이름
    student_score_file = open(student_score_file_name, 'w')
    student_score_csv = csv.writer(student_score_file, 
            delimiter = ',', quotechar = '"', 
            quoting = csv.QUOTE_MINIMAL) # csv파일 생성
    student_score_csv.writerow(['학년', '반', '번호', '점수'])

    for rows in student_list: # 학생 파일 순회
        current_student_grade = int(rows[0]) # 현재 정보
        current_student_class = int(rows[1])
        current_student_number = int(rows[2])
        current_student_answer_list = rows[3:len(rows)] # 현재 답 리스트
        current_student_score = 0 # 현재 학생 점수
        
        # 답 체크
        for index in range(0, len(current_student_answer_list)):
            try: # 답을 입력 안 했을 경우가 존재, 예외처리
                current_student_answer = \
                        int(current_student_answer_list[index]) # 제출 답
                                                           # 이중 답 무시
                current_problem_answer_set = \
                        (answer_list[index+1])[0] # 실제 답
                current_problem_score = \
                        (answer_list[index+1])[1] # 점수
            except ValueError: # int()에서 ValueError가 발생
                pass
            if(current_student_answer 
                    in current_problem_answer_set): # 정답일 경우
                current_student_score = \
                        current_student_score + \
                        current_problem_score # 점수 추가
        
        student_score_csv.writerow([current_student_grade, 
                current_student_class, 
                current_student_number, 
                current_student_score])
    student_score_file.close() # 학생 점수 파일 닫기

    student_answer_rate = dict() # 학생 답안 비율
    for (problem_number, answer_number_list, answer_score) in teacher_list:
        student_answer_rate[int(problem_number)] = dict()
    for rows in student_list: # 학생 파일 순회
        current_student_answer_list = rows[3:len(rows)] # 현재 답 리스트

        for index in range(0, len(current_student_answer_list)):
            try: # 답을 입력하지 않았거나, 이중 답일 경우
                current_student_answer = \
                        int(current_student_answer_list[index])
            except ValueError:
                pass
            (student_answer_rate[index+1])[current_student_answer] = \
                    student_answer_rate[index+1].get( \
                            current_student_answer, 0) \
                    + 1
    print student_answer_rate

    answer_rate_file_name = '문항별정답률.csv' # 결과 파일 이름
    answer_rate_file = open(answer_rate_file_name, 'w')
    answer_rate_csv = csv.writer(answer_rate_file, 
            delimiter = ',' , quotechar = '"', 
            quoting = csv.QUOTE_MINIMAL) # csv파일 생성
    answer_rate_csv.writerow(['문제번호', '답', '정답률', 
            '1번', '2번', '3번', '4번', '5번']) # 결과파일 헤더

    for (problem_number, answer_number_list, answer_score) in teacher_list:
        answer_rate = dict() # 답안 비율 계산
        answer_rate[1] = float( \
                student_answer_rate[int(problem_number)].get(1, 0)) \
                / float( \
                sum(student_answer_rate[int(problem_number)].values()))
        answer_rate[2] = float( \
                student_answer_rate[int(problem_number)].get(2, 0)) \
                / float( \
                sum(student_answer_rate[int(problem_number)].values()))
        answer_rate[3] = float( \
                student_answer_rate[int(problem_number)].get(3, 0)) \
                / float( \
                sum(student_answer_rate[int(problem_number)].values()))
        answer_rate[4] = float( \
                student_answer_rate[int(problem_number)].get(4, 0)) \
                / float( \
                sum(student_answer_rate[int(problem_number)].values()))
        answer_rate[5] = float( \
                student_answer_rate[int(problem_number)].get(5, 0)) \
                / float( \
                sum(student_answer_rate[int(problem_number)].values()))

        current_answer_set = set() # 답 세트
        for answer_number in (answer_number_list.strip()).split(' '):
            current_answer_set.add(int(answer_number))

        answer_string = None # 다중 답을 위한 리스트 계산
        current_answer_list = list(current_answer_set)
        current_answer_list.sort()
        for answer_number in current_answer_list:
            if answer_string != None:
                answer_string = answer_string + ' ' + str(answer_number)
            else:
                answer_string = str(answer_number)

        collect_rate = 0.0 # 정답 비율 계산
        for answer_number in current_answer_set:
            collect_rate = collect_rate + answer_rate[answer_number]

        answer_rate_csv.writerow([int(problem_number),
                answer_string,
                collect_rate,
                answer_rate[1],
                answer_rate[2],
                answer_rate[3],
                answer_rate[4],
                answer_rate[5]]) # 파일로 작성
    answer_rate_file.close() # 답 비율 파일 닫기

    print '계산 완료!'
    print '추가 보완 사항은 개인적으로 연락주세용!\n'


if __name__ == '__main__':
    main()
