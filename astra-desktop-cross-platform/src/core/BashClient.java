package core;

import java.io.*;
import java.util.LinkedList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.Executors;
import java.util.function.Consumer;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * Runs shell commands in Java when ARGS are specified.
 * Created by Soham Kale on 2/20/18
 *
 */
public class BashClient {

     static String[] bash(String... args) {
        boolean isWindows = System.getProperty("os.name")
                .toLowerCase().startsWith("windows");

        ProcessBuilder builder = new ProcessBuilder();

        String[] cmndArgs = new String[args.length + 2];
        System.arraycopy(args, 0, cmndArgs, 2, args.length);
        if (isWindows) {
            System.arraycopy(new String[] {"cmd.exe", "/c"}, 0, cmndArgs, 0, 2);
            builder.command(cmndArgs);
        } else {
            System.arraycopy(new String[] {"sh", "-c"}, 0, cmndArgs, 0, 2);
            builder.command(cmndArgs);
        }

        builder.directory(new File("./Boinc"));

        int exitCode = -1;
        StreamConsumer streamConsumer = new StreamConsumer();
        try {
            Process process = builder.start();
            streamConsumer = new StreamConsumer(process.getInputStream());
            Executors.newSingleThreadExecutor().submit(streamConsumer);
            exitCode = process.waitFor();
        } catch (java.io.IOException io) {
            System.out.println("Unable to start process from process builder");
        } catch (java.lang.InterruptedException ie) {
            System.out.println("Unable to finish process");
        }

        List<String> output;
        synchronized (streamConsumer) {
            if (!streamConsumer.hasData) {
                try {
                    // Wait here for streamConsumer to signal that it has data
                    streamConsumer.wait();
                } catch (InterruptedException e) {
                    return new String[] {};
                }
            }
            // At this point the data will have been made available and is ready to be consumed
            output = streamConsumer.output();
        }
        return output.toArray(new String[output.size()]);
    }

    static void bashPersist(String... args) {
        boolean isWindows = System.getProperty("os.name")
                .toLowerCase().startsWith("windows");

        ProcessBuilder builder = new ProcessBuilder();

        String[] cmndArgs = new String[args.length + 2];
        System.arraycopy(args, 0, cmndArgs, 2, args.length);
        if (isWindows) {
            System.arraycopy(new String[]{"cmd.exe", "/c"}, 0, cmndArgs, 0, 2);
            builder.command(cmndArgs);
        } else {
            System.arraycopy(new String[]{"sh", "-c"}, 0, cmndArgs, 0, 2);
            builder.command(cmndArgs);
        }

        builder.directory(new File("./Boinc"));

        Timer timer = new Timer();
        try {
            Process process = builder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            timer.schedule(new InterruptScheduler(Thread.currentThread()), 3000L);
            int exitCode = process.waitFor();
        } catch (IOException | InterruptedException e) {
            timer.cancel();
        } finally {
            timer.cancel();
        }
    }

    private static class InterruptScheduler extends TimerTask {
        Thread target;

        InterruptScheduler(Thread target) {
            this.target = target;
        }

        @Override
        public void run() {
            target.interrupt();
        }

    }

    private static class StreamConsumer implements Runnable {
        private InputStream inputStream;
        private List<String> output;
        boolean hasData;

        StreamConsumer(InputStream inputStream) {
            this.inputStream = inputStream;
            output = new LinkedList<>();
            hasData = false;
        }

        StreamConsumer() {
            output = new LinkedList<>();
        }
        List<String> output() { return output; }
        Consumer<String> addToOutput = line -> this.output.add(line);

        @Override
        public void run() {
            hasData = false;
            new BufferedReader(new InputStreamReader(inputStream)).lines()
                    .forEach(addToOutput);

            /* Notify any waiting thread that data is now ready */
            synchronized (this) {
                hasData = true;
                notifyAll();
            }
        }
    }

    public static void main(String... args) {
//        String[] output = bash("ls -a; mkdir test");
//        for (String line : output) {
//            System.out.println(line);
//        }

        bashPersist("./boinc -insecure");
    }
}
