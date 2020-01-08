import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;

public class HourGlass {

    // Complete the hourglassSum function below.
    static int hourglassSum(int[][] arr) {
        int max = -Integer.MAX_VALUE;
        int hour = 0;

        for (int i = 1; i < arr.length-1; i++) {
            for (int j = 1; j < arr[i].length-1; j++) {
                hour = arr[i-1][j-1] + arr[i-1][j] + arr[i-1][j+1];
                hour = hour + arr[i][j];
                hour = hour + arr[i+1][j-1] + arr[i+1][j] + arr[i+1][j+1];
                if (max < hour) {
                    max = hour;
                }
            }
        }

        return max;
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        int[][] arr = new int[6][6];

        for (int i = 0; i < 6; i++) {
            String[] arrRowItems = scanner.nextLine().split(" ");
            scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

            for (int j = 0; j < 6; j++) {
                int arrItem = Integer.parseInt(arrRowItems[j]);
                arr[i][j] = arrItem;
            }
        }

        int result = hourglassSum(arr);

        System.out.println(String.valueOf(result));

        scanner.close();
    }
}

