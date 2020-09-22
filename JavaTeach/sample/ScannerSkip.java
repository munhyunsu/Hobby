import java.util.Scanner;


public class ScannerSkip {
    static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        while (scanner.hasNext()) {
            String string = scanner.next();
            scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");
            System.out.println(string);
            double value = scanner.nextDouble();
            scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");
            System.out.println(value);
        }
    }
}
