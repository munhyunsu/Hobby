import java.io.*;
import java.math.*;
import java.text.*;
import java.util.*;
import java.util.regex.*;

public class EqualStack {

    /*
     * Complete the equalStacks function below.
     */
    static int equalStacks(int[] h1, int[] h2, int[] h3) {
        /*
         * Write your code here.
         */
        Stack<Integer> s1=new Stack<Integer>();
        Stack<Integer> s2=new Stack<Integer>();
        Stack<Integer> s3=new Stack<Integer>();
        int sum1=0,sum2=0,sum3=0;
        for (int i = h1.length-1; i>=0; i--) {
            s1.push(h1[i]);
            sum1+=h1[i];
        }
        for (int i=h2.length-1; i>=0; i--) {
            s2.push(h2[i]);
            sum2+=h2[i];
        }
        for (int i=h3.length-1; i>=0;i--) {
            s3.push(h3[i]);
            sum3+=h3[i];
        }
        while (!(sum1==sum2&&sum2==sum3&&sum3==sum1)) {
            if (sum1==0||sum2==0||sum3==0) {
                sum1=0;
                break;
            } else if (sum1>=sum2&&sum1>=sum3) {
                sum1-=s1.peek();
                s1.pop();
            } else if (sum2>=sum1&&sum2>=sum3) {
                sum2-=s2.peek();
                s2.pop();
            } else if (sum3>=sum1&&sum3>=sum2) {
                sum3-=s3.peek();
                s3.pop();
            }
        }
        return sum1;
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        String[] n1N2N3 = scanner.nextLine().split(" ");

        int n1 = Integer.parseInt(n1N2N3[0].trim());

        int n2 = Integer.parseInt(n1N2N3[1].trim());

        int n3 = Integer.parseInt(n1N2N3[2].trim());

        int[] h1 = new int[n1];

        String[] h1Items = scanner.nextLine().split(" ");

        for (int h1Itr = 0; h1Itr < n1; h1Itr++) {
            int h1Item = Integer.parseInt(h1Items[h1Itr].trim());
            h1[h1Itr] = h1Item;
        }

        int[] h2 = new int[n2];

        String[] h2Items = scanner.nextLine().split(" ");

        for (int h2Itr = 0; h2Itr < n2; h2Itr++) {
            int h2Item = Integer.parseInt(h2Items[h2Itr].trim());
            h2[h2Itr] = h2Item;
        }

        int[] h3 = new int[n3];

        String[] h3Items = scanner.nextLine().split(" ");

        for (int h3Itr = 0; h3Itr < n3; h3Itr++) {
            int h3Item = Integer.parseInt(h3Items[h3Itr].trim());
            h3[h3Itr] = h3Item;
        }

        int result = equalStacks(h1, h2, h3);

        System.out.println(result);
        scanner.close();
    }
}
