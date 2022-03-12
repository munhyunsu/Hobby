package org.cs_cnu.morsecode;

import android.util.Log;

import java.util.Map;

public class MorseCodeSpeakerCodeGenerator {

    final String message;
    final Map<String, String> map;

    public MorseCodeSpeakerCodeGenerator(String message, Map<String, String> map) {
        this.message = message;
        this.map = map;
        Log.i("MorseCode", "Created");
    }
}
