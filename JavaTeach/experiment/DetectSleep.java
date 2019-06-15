package class02;

import java.util.Scanner;
import java.util.Arrays;

public class DetectSleep {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String data;
        String[] values;
        int st;
        int hb;

        data = scanner.nextLine();
        while (!data.equals("q")) {
            values = data.split(" ");
            System.out.println(Arrays.toString(values));
            
            st = Integer.parseInt(values[0]);
            hb = Integer.parseInt(values[1]);

            data = scanner.nextLine();

        }
    }
}
