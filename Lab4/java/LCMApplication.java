
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;


public class LCMApplication {
     private static JLabel label = new JLabel("Number of clicks:  0     ");
    private JFrame frame = new JFrame();

     public LCMApplication() {


        // the panel with the button and text
        JPanel panel = new JPanel();
        panel.setBorder(BorderFactory.createEmptyBorder(30, 30, 10, 30));
        panel.setLayout(new GridLayout(0, 1));
        panel.add(label);
        label.setOpaque(true);
        label.setBackground(Color.green);
        label.setText("BREAK OFF");
        label.setForeground(Color.white);
        // set up the frame and display it
        frame.add(panel, BorderLayout.CENTER);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setTitle("GUI");
        frame.pack();
        frame.setVisible(true);
    }
	public static void main(String[] args) {
		new LCMApplication();
        try {

			MySubscriber subscriber = new MySubscriber();
            HeartBeatSignal heartBeatSignal = new HeartBeatSignal();
            heartBeatSignal = subscriber.hearBeat;            
            while(true){
                if(heartBeatSignal.isApplyBreaks()){
                    setBreakInGUI();
                    System.out.println("Break ON");
                }else{
                    setBreakOff();
                }
            }
           
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

    public static void setBreakInGUI(){
        label.setText("BreakON");
        label.setBackground(Color.red);
        label.setForeground(Color.white);
    }

    public static void setBreakOff(){
        label.setText("BreakOFf");
        label.setBackground(Color.green);
        label.setForeground(Color.white);
    }
}