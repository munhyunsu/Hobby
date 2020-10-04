import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;


class CMath <T extends Number> {
    T number;
    public static <T extends Number> T getAverage(ArrayList<T> a) {
        T number;
        for(int i = 0; i < a.size(); i++) {
            number += (T) a.get(i);
        }
        return number / a.size();
    }
}

public class RandomList {
    final static Scanner scanner = new Scanner(System.in);
    public static void main(String[] args) {
        List<Double> dl = new ArrayList<>();
        List<Integer> il = new ArrayList<>();

        dl.add(1.0);
        dl.add(2.0);
        dl.add(3.0);
        dl.add(4.0);

        System.out.println(CMath.getAverage(dl));
    }
}
