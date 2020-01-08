import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;

public class Brackets {

    // Complete the isBalanced function below.
    static String isBalanced(String s) {
        Stack<Character> stack = new Stack<Character>();
        for (char ch: s.toCharArray()) {
            if (ch == '(') {
                stack.push(ch);
            } else if (ch == '{') {
                stack.push(ch);
            } else if (ch == '[') {
                stack.push(ch);
            } else if (ch == ')') {
                if (stack.peek() == '(') {
                    stack.pop();
                } else {
                    return "NO";
                }
            } else if (ch == '}') {
                if (stack.peek() == '{') {
                    stack.pop();
                } else {
                    return "NO";
                }
            } else if (ch == ']') {
                if (stack.peek() == '[') {
                    stack.pop();
                } else {
                    return "NO";
                }
            }
        }
        return "YES";

    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        int t = scanner.nextInt();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        for (int tItr = 0; tItr < t; tItr++) {
            String s = scanner.nextLine();

            String result = isBalanced(s);

            System.out.println(result);           

        }

        scanner.close();
    }
}

