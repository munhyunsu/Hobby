package org.cs_cnu.morsecode;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    static final int sample_rate = 48000;
    static final float frequency = 523.251f;
    static final float unit = 0.1f; // second

    final Map<String, String> map = new HashMap<>();

    private EditText box_text;
    private TextView text_result;
    private Button btn_speaker;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        map.put("A", ".-");    map.put("B", "-...");  map.put("C", "-.-.");
        map.put("D", "-..");   map.put("E", ".");     map.put("F", "..-.");
        map.put("G", "--.");   map.put("H", "....");  map.put("I", "..");
        map.put("J", ".---");  map.put("K", "-.-");   map.put("L", ".-..");
        map.put("M", "--");    map.put("N", "-.");    map.put("O", "---");
        map.put("P", ".--.");  map.put("Q", "--.-");  map.put("R", ".-.");
        map.put("S", "...");   map.put("T", "-");     map.put("U", "..-");
        map.put("V", "...-");  map.put("W", ".--");   map.put("X", "-..-_");
        map.put("Y", "-.--");  map.put("Z", "--..");
        map.put("0", "-----"); map.put("1", ".----"); map.put("2", "..---");
        map.put("3", "...--"); map.put("4", "....-"); map.put("5", ".....");
        map.put("6", "-...."); map.put("7", "--..."); map.put("8", "---..");
        map.put("9", "----.");

        box_text = (EditText) findViewById(R.id.box_text);
        text_result = (TextView) findViewById(R.id.text_result);
        btn_speaker = (Button) findViewById(R.id.btn_speaker);

        // https://developer.android.com/reference/android/view/View#setOnClickListener(android.view.View.OnClickListener)
        btn_speaker.setOnClickListener(new View.OnClickListener() {
            // https://developer.android.com/reference/android/view/View.OnClickListener
            @Override
            public void onClick(View v) {
                String message = box_text.getText().toString();
                Log.i("User input", message);
                if (message.length() > 0) {
                    btn_speaker.setEnabled(false);
                    MorseSpeakerCodeGenerator generator = new MorseSpeakerCodeGenerator(message, map);
                    text_result.setText(generator.getMorseCode());
                    new MorseSpeakerThread(generator, new MorseSpeakerThread.MorseSpeakerCallback() {
                        @Override
                        public void onProgress(int current, int total) {
                        }

                        @Override
                        public void onDone() {
                            btn_speaker.setEnabled(true);
                        }
                    },
                            sample_rate, frequency, unit).start();
                }
            }
        });
    }
}