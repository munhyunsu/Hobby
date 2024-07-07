import java.util.Scanner;
import java.util.Set;
import java.util.HashSet;


class SetPrint {
    private static final Scanner scanner = new Scanner(System.in);

    public static void printSet(Set<Integer> s) {
        Integer[] a = new Integer[s.size()];
        s.toArray(a);
        for (int i = 0; i < a.length; i++) {
            System.out.print(a[i]);
            if (i != a.length-1) {
                System.out.print(" ");
            }
        }
        System.out.println("");
    }

    public static void main(String[] args) {
        String line = scanner.nextLine();
        String[] str1 = line.split(" ");
        int[] addr1 = new int[str1.length];
        line = scanner.nextLine();
        String[] str2 = line.split(" ");
        int[] addr2 = new int[str2.length];

        Set<Integer> a = new HashSet<Integer>();
        for (int i = 0; i < str1.length; i++) {
            a.add(Integer.parseInt(str1[i]));
        }
        Set<Integer> b = new HashSet<Integer>();
        for (int i = 0; i < str2.length; i++) {
            b.add(Integer.parseInt(str2[i]));
        }

        Set<Integer> union = new HashSet<Integer>(a); 
        union.addAll(b);
        printSet(union); 
  
        // To find intersection 
        Set<Integer> intersection = new HashSet<Integer>(a); 
        intersection.retainAll(b); 
        printSet(intersection);
  
        // To find the symmetric difference 
        Set<Integer> difference = new HashSet<Integer>(a); 
        difference.removeAll(b); 
        printSet(difference); 

    }
}
