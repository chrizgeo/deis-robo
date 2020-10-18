import lcm.lcm.*;
import exlcm.*;

import java.io.*;

public class MySubscriber implements LCMSubscriber
{
    LCM lcm;
    HeartBeatSignal hearBeat = new HeartBeatSignal();

    public MySubscriber()
        throws IOException
    {
        try{
            this.lcm = new LCM();
            this.lcm.subscribe("HEARTBEAT", this);
        }
          catch (IOException ex) {
            System.out.println("Exception: " + ex);
        }
        
    }

    public void messageReceived(LCM lcm, String channel, LCMDataInputStream ins)
    {
        System.out.println("Received message on channel " + channel);

        try {
            if (channel.equals("HEARTBEAT")) {
                example_t msg = new example_t(ins);
                
                hearBeat.setTimestamp(msg.timestamp);
                hearBeat.setStatus(msg.mode);
                hearBeat.setMoving(msg.isMoving);
                hearBeat.setApplyBreaks(msg.apply_brakes);
            }

        } catch (IOException ex) {
            System.out.println("Exception: " + ex);
        }
    }
}
