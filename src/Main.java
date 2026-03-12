import java.util.HashMap;

public class Main {
    public static void main (String[] args) {

    }

    /* Clean up input text by stripping whitespace, lowercasing, and removing anything that is not a letter */
    public String clean(String text) {
        String unwanted = "[-+^\\[]]@#$%&*{}|/";
        return text.toLowerCase().trim().replaceAll(unwanted, "");
    }

    public HashMap<String, Integer> buildMatrix(String words) {
        HashMap<String, Integer> vocab = new HashMap<String, Integer>();
        String[] arr = words.split(" ");
        for (int i = 0; i < arr.length; i++) {
            vocab.put(arr[i], i);
        }
        return vocab;
    }
}