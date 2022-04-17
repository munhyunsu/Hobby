package org.cs_cnu.morsecode;

import android.util.Log;

import java.util.Map;

public class MorseMicrophoneTextGenerator {

    final String morse_code;
    final Map<String, String> map;
    final String text;

    public MorseMicrophoneTextGenerator(String morse_code, Map<String, String> map) {
        this.morse_code = morse_code;
        this.map = map;

// Need to edit below!
        StringBuilder sb = new StringBuilder();
        sb.append("CSE");
// Need to edit abobe!

        this.text = sb.toString();
        Log.i("Sound input", text);
    }

    public String getText() {
        return this.text;
    }
}
