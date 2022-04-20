package org.cs_cnu.morsecode;

import android.annotation.SuppressLint;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;

public class MorseMicrophoneThread extends Thread {
    public interface MorseMicrophoneCallback {
        void onProgress(String value);
        void onDone(String value);
    }

    final int sample_rate;
    final float frequency;
    final float unit;
    final int unit_size;
    final int buffer_size;

    final MorseMicrophoneThread.MorseMicrophoneCallback callback;

    public MorseMicrophoneThread(MorseMicrophoneThread.MorseMicrophoneCallback callback,
                                 int sample_rate, float frequency, float unit) {
        this.callback = callback;
        this.sample_rate = sample_rate;
        this.frequency = frequency;
        this.unit = unit;
        this.unit_size = (int) Math.ceil(this.sample_rate * this.unit);
        this.buffer_size = (int) AudioRecord.getMinBufferSize(sample_rate, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT);
        setPriority(Thread.MAX_PRIORITY);
    }

    @Override
    public void run() {
        @SuppressLint("MissingPermission") final AudioRecord record = new AudioRecord(
                MediaRecorder.AudioSource.DEFAULT,
                this.sample_rate,
                AudioFormat.CHANNEL_IN_MONO,
                AudioFormat.ENCODING_PCM_16BIT,
                2 * sample_rate);

        final short[] samples = new short[unit_size];

        record.startRecording();

        while (true) {
            record.stop();
            record.release();
            break;
        }
    }
}
