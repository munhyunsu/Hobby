def main():
    # 사용자 입력 파트
    user_input = input('Input the text (Unicode): ').strip()
    print(f'User input: {user_input}')

    # str => hex 변경 파트
    byte_hex = user_input.encode('utf-8')
    byte_string = byte_hex.hex().upper()
    print(f'byte_string: {byte_string}')

    # 여기서 byte_string을 서로 통신했을 것!
    # 이 아래의 byte_string은 통신으로 받은 str 이라고 가정

    # byte_string => str 변경 파트
    client_byte_hex = bytes.fromhex(byte_string)
    client_byte_string = client_byte_hex.hex().upper()
    print(f'client_byte_string: {client_byte_string}')


    # str => 사용자 출력
    client_output = client_byte_hex.decode('utf-8')
    print(f'User output: {client_output}')


if __name__ == '__main__':
    main()

