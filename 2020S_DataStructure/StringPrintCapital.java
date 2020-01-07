import java.util.Scanner;

class StringPrintCapital {

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        String line = scanner.nextLine();
        int str_cnt = Integer.parseInt(line);

        line = scanner.nextLine();
        String[] repeat = line.split(" ");

        for (int i = 0; i < str_cnt; i++) {
            int repeat_cnt = Integer.parseInt(repeat[i]);
            line = scanner.nextLine();
            for (int j = 0; j < repeat_cnt; j++) {
                System.out.println(line.toUpperCase());
            }
        }
    }
}

