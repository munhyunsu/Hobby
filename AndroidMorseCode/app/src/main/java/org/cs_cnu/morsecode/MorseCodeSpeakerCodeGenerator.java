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
}
