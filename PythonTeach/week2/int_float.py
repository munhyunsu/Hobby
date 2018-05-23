num = input('정수 혹은 소수를 입력하세요: ')
print(type(num))

float_num = float(num)
print(type(float_num))
print('입력한 숫자의 소수형: {0}'.format(float_num))

int_num = int(float_num)
print(type(int_num))
print('입력한 숫자의 정수형: {0}'.format(int_num))

