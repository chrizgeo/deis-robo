import java.io.*;

import lcm.lcm.*;
import exlcm.*;

public class SendMessage
{
    public static void main(String args[])
    {
        try {
            LCM lcm = new LCM();

            example_t msg = new example_t();

            msg.timestamp = System.nanoTime();

            msg.mode = 1;
            msg.isMoving = true;
            msg.apply_brakes = true;

            lcm.publish ("HEARTBEAT", msg);
        } catch (IOException ex) {
            System.out.println("Exception: " + ex);
        }
    }
}
