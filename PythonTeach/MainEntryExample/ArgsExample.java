public class ArgsExample {
    public static void main(String[] args) {
        int x = Integer.parseInt(args[0]);
        int y = Integer.parseInt(args[1]);

        System.out.println(String.format("%d + %d = %d", x, y, sum(x, y)));
    }

    public static int sum(int a, int b) {
        return a+b;
    }
}
