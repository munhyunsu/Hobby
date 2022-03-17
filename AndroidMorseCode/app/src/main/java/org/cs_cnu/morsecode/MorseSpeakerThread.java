package org.cs_cnu.morsecode;

public class MorseSpeakerThread extends Thread {

    public interface MorseSpeakerCallback {
        void onProgress(int current, int total);
        void onDone();
    }

    public interface MorseSpeakerIterator extends Iterable<String> {
        int getSize();
    }

    public MorseSpeakerThread(MorseSpeakerIterator iterator, MorseSpeakerCallback callback) {
        setPriority(Thread.MAX_PRIORITY);
    }
}
