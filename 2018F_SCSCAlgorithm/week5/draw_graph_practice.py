import time
import matplotlib.pyplot as plt


def func_logn(num_loop):
    while num_loop > 0:
        num_loop = num_loop // 2


def func_n(num_loop):
    for index in range(0, num_loop):
        pass


def func_n2(num_loop):
    for index in range(0, num_loop):
        for index2 in range(0, num_loop):
            pass


def main():
    x_data = range(0, 101, 1)  # X 축
    y_data1 = list()  # Y축1
    y_data2 = list()  # Y축2
    y_data3 = list()  # Y축3

    for x in x_data:  # X축 만큼 순환
        # Y1
        start_time = time.time()
        func_logn(x)
        end_time = time.time()
        execution_time = end_time - start_time
        y_data1.append(execution_time)

        # Y2
        start_time = time.time()
        func_n(x)
        end_time = time.time()
        execution_time = end_time - start_time
        y_data2.append(execution_time)

        # Y3
        start_time = time.time()
        func_n2(x)
        end_time = time.time()
        execution_time = end_time - start_time
        y_data3.append(execution_time)

    # 차트 그리기
    plt.plot(x_data, y_data1, 'r.-', label='Log N')
    plt.plot(x_data, y_data2, 'g.-', label='N')
    plt.plot(x_data, y_data3, 'b.-', label='N**2')
    # 범례 추가
    plt.legend(bbox_to_anchor=(0.05, 0.95), loc=2, borderaxespad=0.0)
    plt.title('Time Complexity')  # 제목
    plt.ylabel('Execution time (sec)')  # Y축
    plt.xlabel('N')  # X축
    # 차트 저장 및 표시
    plt.savefig('time_complexity.png', bbox_inches='tight')  # 차트 저장
    # plt.show() # 차트 표시
    plt.close()  # 차트 닫기


if __name__ == '__main__':
    main()
