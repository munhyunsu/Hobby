user_age = int(input('나이: '))

if (user_age > 15) and (user_age%2 == 0):
    print('당신의 나이는 15살보다 많고 짝수이군요!')
elif (user_age > 15) and (user_age%2 == 1):
    print('당신의 나이는 15살보다 많고 홀수이군요!')
else:
    print('당신의 나이는 15살보다 적군요.')

