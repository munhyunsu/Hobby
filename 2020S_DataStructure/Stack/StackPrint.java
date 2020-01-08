import java.io.*;
import java.util.*;

public class StackPrint {

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        String line = scanner.nextLine();
        int cnt = Integer.parseInt(line);

        Stack<Integer> stack = new Stack<Integer>();
        stack.push(-Integer.MAX_VALUE);
        int buff = 0;


        for (int i = 0; i < cnt; i++) {
            line = scanner.nextLine();
            String str[] = line.split(" ");
            int cmd = Integer.parseInt(str[0]);
            if (cmd == 1) {
                int value = Integer.parseInt(str[1]);
                if (stack.peek() < value) {
                    stack.push(value);
                } else {
                    stack.push(stack.peek());
                }
            } else if (cmd == 2) {
                stack.pop();
            } else if (cmd == 3) {
                System.out.println(stack.peek());
            }
        }
    }
}


