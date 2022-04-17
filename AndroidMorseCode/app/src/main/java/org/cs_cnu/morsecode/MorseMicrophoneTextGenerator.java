package org.cs_cnu.morsecode;

import java.util.Map;

public class MorseMicrophoneTextGenerator {

    final String morse_code;
    final Map<String, String> map;
    final String text;

    public MorseMicrophoneTextGenerator(String morse_code, Map<String, String> map) {
        this.morse_code = morse_code;
        this.map = map;

        this.text = "";
    }

    public String getText() {
        return this.text;
    }
}
