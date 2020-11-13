public class HeartBeatSignal {

	long timestamp;
    byte status;
    boolean isMoving;
    boolean applyBreaks;
	public long getTimestamp() {
		return timestamp;
	}
	public void setTimestamp(long timestamp) {
		this.timestamp = timestamp;
	}
	public byte getStatus() {
		return status;
	}
	public void setStatus(byte status) {
		this.status = status;
	}
	public boolean isMoving() {
		return isMoving;
	}
	public void setMoving(boolean isMoving) {
		this.isMoving = isMoving;
	}
	public boolean isApplyBreaks() {
		return applyBreaks;
	}
	public void setApplyBreaks(boolean applyBreaks) {
		this.applyBreaks = applyBreaks;
	}
    
    
}