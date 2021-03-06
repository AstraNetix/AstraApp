package core;

import javafx.event.ActionEvent;
import javafx.scene.Cursor;
import javafx.scene.control.Button;

import javax.crypto.*;
import javax.crypto.spec.SecretKeySpec;
import javafx.event.EventHandler;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Formatter;
import java.util.HashMap;
import java.util.Map;

/**
 * Copyright (c) 2018 Astra International. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * Various helpful utilities.
 * Created by Soham Kale on 2/20/18
 *
 */
public class Utils {
    /** Returns the SHA-1 hash of the concatenation of VALS, which may
     *  be any mixture of byte arrays and Strings. */
    static String sha1(Object... vals) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-1");
            for (Object val : vals) {
                if (val instanceof byte[]) {
                    md.update((byte[]) val);
                } else if (val instanceof String) {
                    md.update(((String) val).getBytes(StandardCharsets.UTF_8));
                } else {
                    throw new IllegalArgumentException("improper type to sha1");
                }
            }
            Formatter result = new Formatter();
            for (byte b : md.digest()) {
                result.format("%02x", b);
            }
            return result.toString();
        } catch (NoSuchAlgorithmException excp) {
            throw new IllegalArgumentException("System does not support SHA-1");
        }
    }

    static void writeObject(File file,
                               Serializable obj) {
        byte[] contents = serialize(obj);
        try {
            SecretKeySpec sks = new SecretKeySpec(cipherPassword.getBytes(), outputAlgorithm);
            Cipher cipher = Cipher.getInstance(outputAlgorithm);
            cipher.init(Cipher.ENCRYPT_MODE, sks);
            SealedObject sealedObject = new SealedObject(obj, cipher);

            CipherOutputStream cos =
                    new CipherOutputStream(new BufferedOutputStream(new FileOutputStream(file)), cipher);
            ObjectOutputStream outputStream = new ObjectOutputStream(cos);
            outputStream.writeObject(sealedObject);

            cos.close();
            outputStream.close();
        } catch (IOException | ClassCastException excp) {
            throw new IllegalArgumentException(excp.getMessage());
        } catch (NoSuchAlgorithmException | NoSuchPaddingException |
                InvalidKeyException | IllegalBlockSizeException excp) {
            excp.printStackTrace();
        }
    }

    static <T extends Serializable> T readObject(File file,
                                                 Class<T> expectedClass) {
        T object = null;
        try {
            SecretKeySpec sks = new SecretKeySpec(cipherPassword.getBytes(), outputAlgorithm);
            Cipher cipher = Cipher.getInstance(outputAlgorithm);
            cipher.init(Cipher.DECRYPT_MODE, sks);

            CipherInputStream cipherInputStream =
                    new CipherInputStream( new BufferedInputStream(new FileInputStream(file)), cipher);
            ObjectInputStream inputStream = new ObjectInputStream( cipherInputStream );
            SealedObject sealedObject = (SealedObject) inputStream.readObject();
            object = expectedClass.cast(sealedObject.getObject(cipher));

            inputStream.close();
            cipherInputStream.close();
        } catch (IOException | ClassCastException
                | ClassNotFoundException excp) {
            throw new IllegalArgumentException(excp.getMessage());
        } catch (NoSuchAlgorithmException | NoSuchPaddingException |
                InvalidKeyException | IllegalBlockSizeException | BadPaddingException excp) {
            excp.printStackTrace();
        }
        return object;
    }

    /** Returns a byte array containing the serialized contents of OBJ. */
    private static byte[] serialize(Serializable obj) {
        try {
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            ObjectOutputStream objectStream = new ObjectOutputStream(stream);
            objectStream.writeObject(obj);
            objectStream.close();
            return stream.toByteArray();
        } catch (IOException excp) {
            excp.printStackTrace();
        } return new byte[] {};
    }

    static void setupButton(Button button,
                            EventHandler<ActionEvent> eventHandler,
                            Manager manager) {
        button.setOnMouseEntered(event -> manager._scene.setCursor(Cursor.HAND));
        button.setOnAction(eventHandler);
        button.setOnMouseExited(event -> manager._scene.setCursor(Cursor.DEFAULT));
    }

    static String convertToISO8601(String rawDate) {
        return String.format("%s-%s-%sT%sZ",
                rawDate.substring(20, 25),
                months.get(rawDate.substring(4, 7)),
                rawDate.substring(8, 10),
                rawDate.substring(11, 19)
        );
    }

    private static final Map<String, String> months = new HashMap<String, String>() {{
        put("Jan", "01");  put("Feb", "02");  put("Mar", "03");  put("Apr", "04");
        put("May", "05");  put("Jun", "06");  put("Jul", "07");  put("Aug", "08");
        put("Sep", "09");  put("Oct", "10");  put("Nov", "11");  put("Dec", "12");
    }};

    // TODO: change in production (must be 16 bytes)
    private static final String cipherPassword = "9np9l2'a=e/c]v`5";
    private static final String outputAlgorithm = "AES";

}

