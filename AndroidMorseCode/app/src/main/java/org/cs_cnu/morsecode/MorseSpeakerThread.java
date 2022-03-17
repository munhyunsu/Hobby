package org.cs_cnu.morsecode;

public class MorseSpeakerThread extends Thread {

    public interface MorseSpeakerIterator extends Iterable<String> {
        int getSize();
    }

    public MorseSpeakerThread() {
        setPriority(Thread.MAX_PRIORITY);
    }
}
