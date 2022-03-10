package org.cs_cnu.morsecode;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    private EditText box_text;
    private Button btn_speaker;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        box_text = (EditText) findViewById(R.id.box_text);
        btn_speaker = (Button) findViewById(R.id.btn_speaker);

        // https://developer.android.com/reference/android/view/View#setOnClickListener(android.view.View.OnClickListener)
        btn_speaker.setOnClickListener(new View.OnClickListener() {
            // https://developer.android.com/reference/android/view/View.OnClickListener
            @Override
            public void onClick(View v) {
                String message = box_text.getText().toString();
                Log.i("User input", message);
            }
        });
    }
}