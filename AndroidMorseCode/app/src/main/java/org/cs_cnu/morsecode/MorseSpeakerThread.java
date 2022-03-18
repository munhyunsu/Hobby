package org.cs_cnu.morsecode;

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

    }
}
