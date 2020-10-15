import java.util.Scanner;

public class Template {
    static final Scanner scanner = new Scanner(System.in);
    static boolean debug = false;

    public static void main(String[] args) {
        if(args.length > 0) {
            if(args[0].toUpperCase().equals("DEBUG")) {
                debug = true;
            }
        }
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");
    }

}

