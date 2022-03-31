import java.util.Scanner;
import java.math.BigInteger;
import java.io.UnsupportedEncodingException;

import java.nio.ByteBuffer;


public class JavaUnicode {

    static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        // 사용자 입력 파트
        System.out.print("Input the text (Unicode): ");
        String userInput = scanner.nextLine().strip();
        System.out.println("User input: " + userInput);

        // String => hexString 변경 파트
        byte[] byteHex = new byte[0];
        try {
            byteHex = userInput.getBytes("UTF-8");
        } catch (UnsupportedEncodingException e) {
            System.out.println("Exception: " + e.toString());
        }
        String byteString = new BigInteger(1, byteHex).toString(16).toUpperCase();
        System.out.println("byteHex: " + byteString);

        // 여기서 byteString을 서로 통신했을 것!
        // 이 아래의 byteString은 통신으로 받은 String 이라고 가정

        // hexString => String 변경 파트
        byte[] clientByteHex = new byte[byteString.length()/2];
        for (int i = 0; i < clientByteHex.length; i++) {
            int index = i * 2;
            clientByteHex[i] = (byte) Integer.parseInt(byteString.substring(index, index+2), 16);
        }
        String clientByteString = new BigInteger(1, clientByteHex).toString(16).toUpperCase();
        System.out.println("clientByteString: " + clientByteString);

        // String => 사용자 출력
        String clientOutput = "";
        try {
            clientOutput = new String(clientByteHex, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            System.out.println("Exception: " + e.toString());
        }
        System.out.println("User output: " + clientOutput);
    }
}
