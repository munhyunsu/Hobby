package org.cs_cnu.morsecode;

import android.util.Log;

import java.util.Map;

public class MorseCodeSpeakerCodeGenerator {

    final String message;
    final Map<String, String> map;
    final String morse_code;

    public MorseCodeSpeakerCodeGenerator(String message, Map<String, String> map) {
        this.message = message;
        this.map = map;

// Need to edit below!
        StringBuilder sb = new StringBuilder();
        sb.append("-.-. ... .");
// Need to edit above!

        this.morse_code = sb.toString();
        Log.i("MorseCode", "Created");
    }

    public String getMorseCode() {
        return this.morse_code;
    }

    @Override
    public int getSize() {
        int size = 0;
        for (int i = 0; i < this.morse_code.length(); i++) {
            char ch = this.morse_code.charAt(i);
            if (ch == '/') {
                size = size + 1;
            } else if (ch == ' ') {
                size = size + 1;
            } else if (ch == '.') {
                size = size + 1;
            } else if (ch == '-') {
                size = size + 3;
            }
        }
        size = size + this.morse_code.length();
        return size;
    }
}
