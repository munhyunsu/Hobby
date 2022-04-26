package org.cs_cnu.morsecode;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
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
    private Button btn_microphone;
    private ProgressBar pbar_duration;

    // Requesting permission to RECORD_AUDIO
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;
    private boolean permissionToRecordAccepted = false;
    private String [] permissions = {Manifest.permission.RECORD_AUDIO};

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode){
            case REQUEST_RECORD_AUDIO_PERMISSION:
                permissionToRecordAccepted = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                break;
        }
        if (!permissionToRecordAccepted ) finish();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, permissions, REQUEST_RECORD_AUDIO_PERMISSION);
        }

        map.put("0", "..-");
        map.put("1", ".---");
        map.put("2", "-..-");
        map.put("3", "-...");
        map.put("4", "----");
        map.put("5", "-.--");
        map.put("6", ".-..");
        map.put("7", ".-.-");
        map.put("8", "-.-.");
        map.put("9", "---.");
        map.put("A", "....-");
        map.put("B", "--..");
        map.put("C", ".....");
        map.put("D", "--.-");
        map.put("E", ".--.");
        map.put("F", "...-");

        box_text = (EditText) findViewById(R.id.box_text);
        text_result = (TextView) findViewById(R.id.text_result);
        btn_speaker = (Button) findViewById(R.id.btn_speaker);
        btn_microphone = (Button) findViewById(R.id.btn_microphone);
        pbar_duration = (ProgressBar) findViewById(R.id.pbar_duration);

        // https://developer.android.com/reference/android/view/View#setOnClickListener(android.view.View.OnClickListener)
        btn_speaker.setOnClickListener(new View.OnClickListener() {
            // https://developer.android.com/reference/android/view/View.OnClickListener
            @Override
            public void onClick(View v) {
                String message = box_text.getText().toString();
                Log.i("User input", message);
                if (message.length() > 0) {
                    btn_speaker.setEnabled(false);
                    btn_microphone.setEnabled(false);
                    MorseSpeakerCodeGenerator generator = new MorseSpeakerCodeGenerator(message, map);
                    text_result.setText(generator.getMorseCode());
                    new MorseSpeakerThread(generator, new MorseSpeakerThread.MorseSpeakerCallback() {
                        @Override
                        public void onProgress(int current, int total) {
                            pbar_duration.setMax(total);
                            pbar_duration.setProgress(current);
                        }

                        @Override
                        public void onDone() {
                            btn_speaker.setEnabled(true);
                            btn_microphone.setEnabled(true);
                            pbar_duration.setProgress(0);
                        }
                    },
                            sample_rate, frequency, unit).start();
                }
            }
        });

        btn_microphone.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                btn_speaker.setEnabled(false);
                btn_microphone.setEnabled(false);
                new MorseMicrophoneThread(new MorseMicrophoneThread.MorseMicrophoneCallback() {
                    @Override
                    public void onProgress(String value) {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                text_result.setText(value);
                            }
                        });
                    }

                    @Override
                    public void onDone(String value) {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                String morse_code = value;
                                text_result.setText(value);
                                MorseMicrophoneTextGenerator generator = new MorseMicrophoneTextGenerator(morse_code, map);
                                String text = generator.getText();
                                box_text.setText(text);
                                btn_speaker.setEnabled(true);
                                btn_microphone.setEnabled(true);
                            }
                        });
                    }
                },
                        sample_rate, frequency, unit).start();
            }
        });
    }
}