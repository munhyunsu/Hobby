package org.cs_cnu.morsecode;

import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.util.Log;

public class MorseSpeakerThread extends Thread {

    public interface MorseSpeakerCallback {
        void onProgress(int current, int total);
        void onDone();
    }

    public interface MorseSpeakerIterator extends Iterable<String> {
        int getSize();
    }

    final int sample_rate;
    final float frequency;
    final float unit;
    final int unit_size;

    final MorseSpeakerIterator iterator;
    final MorseSpeakerCallback callback;

    public MorseSpeakerThread(MorseSpeakerIterator iterator, MorseSpeakerCallback callback,
                              int sample_rate, float frequency, float unit) {
        this.iterator = iterator;
        this.callback = callback;
        this.sample_rate = sample_rate;
        this.frequency = frequency;
        this.unit = unit;
        this.unit_size = (int) Math.ceil(this.sample_rate * this.unit);
        setPriority(Thread.MAX_PRIORITY);
    }

    @Override
    public void run() {
        final int morse_size = iterator.getSize();
        final int array_size = (morse_size+1)*unit_size; // add last silence

        final AudioTrack track = new AudioTrack(
                AudioManager.STREAM_MUSIC,
                sample_rate,
                AudioFormat.CHANNEL_OUT_MONO,
                AudioFormat.ENCODING_PCM_16BIT,
                2*sample_rate,
                AudioTrack.MODE_STREAM
        );

        final short[] samples = new short[array_size];
        Log.i("Size", "MorseSize: " + Integer.toString(morse_size) +
                "  UnitSize: " + Integer.toString(unit_size) +
                "  ArraySize: " + Integer.toString(array_size));
        int ptr = 0;
// Need to edit below!
        for (String str : iterator) {
            switch (str) {
                case ".":
                    for (int i = 0; i < unit_size; i++) {
                        samples[ptr] = (short) (Short.MAX_VALUE * Math.sin(2 * Math.PI * frequency * i / sample_rate));
                        ptr = ptr + 1;
                    }
                    break;
                case "-":
                    for (int i = 0; i < unit_size*3; i++) {
                        samples[ptr] = (short) (Short.MAX_VALUE * Math.sin(2 * Math.PI * frequency * i / sample_rate));
                        ptr = ptr + 1;
                    }
                    break;
            }
            for (int i = 0; i < unit_size; i++) {
                samples[ptr] = (short) 0;
                ptr = ptr + 1;
            }
        }
// Need to edit above!
        track.write(samples, 0, samples.length);

    }
}
