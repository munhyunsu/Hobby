import java.util.Scanner;
import java.util.HashMap;

class WordCount {
    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        String line = scanner.nextLine();
        int line_cnt = Integer.parseInt(line);

        HashMap<String, Integer> wordCount = new HashMap<>();

        for (int i = 0; i < line_cnt; i++) {
            line = scanner.nextLine();
            String[] str = line.split(" ");
            for (String s: str) {
                if (wordCount.containsKey(s)) {
                    wordCount.put(s, wordCount.get(s)+1);
                } else {
                    wordCount.put(s, 1);
                }
            }
        }

        int max = 0;
        for (HashMap.Entry<String, Integer> entry: wordCount.entrySet()) {
            if (max < entry.getValue()) {
                max = entry.getValue();
            }
        }

        System.out.println(max);

    }
}
