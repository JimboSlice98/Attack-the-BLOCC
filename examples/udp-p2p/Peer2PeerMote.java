package org.contikios.cooja.motes;

import java.awt.Container;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import org.contikios.cooja.AbstractionLevelDescription;
import org.contikios.cooja.COOJARadioPacket;
import org.contikios.cooja.ClassDescription;
import org.contikios.cooja.Cooja;
import org.contikios.cooja.Mote;
import org.contikios.cooja.MoteTimeEvent;
import org.contikios.cooja.MoteType;
import org.contikios.cooja.RadioPacket;
import org.contikios.cooja.Simulation;
import org.contikios.cooja.interfaces.ApplicationRadio;
import org.contikios.cooja.motes.DisturberMoteType.DisturberMote;

/**
 * Peer-to-peer mote
 *
 * @author James Helsby
 */

public class Peer2PeerMote extends AbstractApplicationMote {
  private ApplicationRadio radio;
  private Random rd;

  private static final long TRANSMISSION_DURATION = Simulation.MILLISECOND*5;                               // UDP broadcast time: 5ms
  private static final long SEND_INTERVAL = Simulation.MILLISECOND*(1000*60 - 5) - TRANSMISSION_DURATION;   // Send request every 60 seconds
  private static final long MS = Simulation.MILLISECOND;
  private static final int TTL = 1000;
  private static final int LOG_LENGTH = 50;
  private static final int LOGTIME_LENGTH = 30;
  private long txCount = 0;
  private Map<String, Long> msgCache = new HashMap<>();

  public Peer2PeerMote(MoteType moteType, Simulation simulation) throws MoteType.MoteTypeCreationException {
    super(moteType, simulation);
  }
  

  protected void execute(long time) {
    // System.out.println("Mote " + getID() + " execute() function called");
    if (radio == null) {
      radio = (ApplicationRadio) getInterfaces().getRadio();
      rd = getSimulation().getRandomGenerator();
    }
    schedulePeriodicPacket(1000*MS*getID());
  }

  
  @Override
  public void receivedPacket(RadioPacket p) {
    String data = new String(p.getPacketData(), java.nio.charset.StandardCharsets.UTF_8);    
    String[] parts = data.split("\\|");
    if (parts.length != 5) {
      return;
    }

    try {
      long messageNum = Long.parseLong(parts[0]);
      int originNode = Integer.parseInt(parts[1]);
      int attestNode = Integer.parseInt(parts[2]);
      long timeOfBroadcast = Long.parseLong(parts[3]);
      int fromNode = Integer.parseInt(parts[4]);
      String logMsg = "Rx: '" + messageNum + "|" + originNode + "|" + attestNode + "|" + timeOfBroadcast + "' from node: '" + fromNode + "'";
      String key = messageNum + "|" + originNode + "|" + attestNode;

      // Check to see if the mote has received this packet before
      if (msgCache.containsKey(key)) {
        // logf(logMsg, "Duplicate");
        return;
      }

      msgCache.put(key, timeOfBroadcast);
      
      // Handle incomming attestations
      if (attestNode != 0 && originNode != getID()) {
        // logf(logMsg, "Rebroadcast attestation");
        broadcastPacket(messageNum, originNode, attestNode, timeOfBroadcast, TTL, 1);
        return;
      }
      else if (attestNode != 0) {
        logf(logMsg, "Attestation received");
        return;
      }

      // Handle incomming messages
      // logf(logMsg, "Rebroadcast message");
      broadcastPacket(messageNum, originNode, attestNode, timeOfBroadcast, TTL, 1);

      // Create new attestation
      timeOfBroadcast = getSimulation().getSimulationTime();
      key = messageNum + "|" + originNode + "|" + getID();
      // logf("Ax: '" + key + "|" + timeOfBroadcast, null);
      msgCache.put(key, timeOfBroadcast);
      broadcastPacket(messageNum, originNode, getID(), timeOfBroadcast, TTL, 1);

    } catch (NumberFormatException e) {
      System.out.println("Mote " + getID() + " received bad data: " + e);
    }
  }


  private void schedulePeriodicPacket(long timeOffset) {
    getSimulation().scheduleEvent(new MoteTimeEvent(this) {
      @Override
      public void execute(long t) {
        long messageNum = txCount;
        int originNode = getID();
        int attestNode = 0;
        long timeOfBroadcast = getSimulation().getSimulationTime();

        String data = messageNum + "|" + originNode + "|" + attestNode;
        logf("Tx: " + "'" + data + "|" + timeOfBroadcast + "'", null);
        msgCache.put(data, timeOfBroadcast);
        txCount++;

        broadcastPacket(messageNum, originNode, attestNode, timeOfBroadcast, TTL, 1);
        schedulePeriodicPacket(0);
      }
    }, getSimulation().getSimulationTime() + SEND_INTERVAL + timeOffset);
  }


  private void broadcastPacket(long messageNum, int originNode, int attestNode, long timeOfBroadcast, int ttl, int timeOffset) {
    if (ttl <= 0) {
      System.out.println(formatTime(getSimulation().getSimulationTimeMillis()) + "  ID " + getID() + ": TTL expired for " + messageNum + "|" + originNode + "|" + attestNode);
      return;
    }

    // System.out.println(formatTime(getSimulation().getSimulationTimeMillis()) + "  ID " + getID() + ": scheduling transmission of " + messageNum + "|" + originNode + "|" + attestNode
    //   + " for execution at " + formatTime(getSimulation().getSimulationTimeMillis() + timeOffset));
  
    getSimulation().scheduleEvent(new MoteTimeEvent(this) {
      @Override
      public void execute(long t) {
        if (radio.isTransmitting() || radio.isReceiving() || radio.isInterfered()) {
          int randomDelay = rd.nextInt(50);
          // System.out.println(formatTime(getSimulation().getSimulationTimeMillis()) + "  ID " + getID() + ": interfered, rescheduling transmission of " + messageNum + "|" + originNode + "|" + attestNode
          //   + " with delay " + randomDelay + " ms and new TTL " + (ttl - randomDelay));
          broadcastPacket(messageNum, originNode, attestNode, timeOfBroadcast, ttl, randomDelay);
          return;
        }
  
        // System.out.println(formatTime(getSimulation().getSimulationTimeMillis()) + "  ID " + getID() + ": transmitting " + messageNum + "|" + originNode + "|" + attestNode + " with TTL " + ttl);  
        String data = messageNum + "|" + originNode + "|" + attestNode + "|" + timeOfBroadcast + "|" + getID();
        radio.startTransmittingPacket(new COOJARadioPacket(data.getBytes(StandardCharsets.UTF_8)), TRANSMISSION_DURATION);
      }
    }, getSimulation().getSimulationTime() + timeOffset*MS);
  }

  
  private void logf(String logMsg, String additionalMsg) {
    String logData;
    if (additionalMsg != null) {
      logData = String.format("%-" + LOG_LENGTH + "s", logMsg) + " -> " + additionalMsg;
    }
    else {
      logData = logMsg;
    }
    log(logData);
    System.out.println(
      String.format(
        "%-" + LOGTIME_LENGTH + "s", formatTime(getSimulation().getSimulationTimeMillis()) + "  ID: " + getID()
      ) + "  " + logData
    );
  }


  public static String formatTime(long milliseconds) {
    long mins = milliseconds / 60000;
    long secs = (milliseconds % 60000) / 1000;
    long millis = milliseconds % 1000;

    String paddedSecs = String.format("%02d", secs);
    String paddedMillis = String.format("%03d", millis);

    return mins + ":" + paddedSecs + "." + paddedMillis;
  }


  @Override
  public void sentPacket(RadioPacket p) {
  }
  
  @Override
  public String toString() {
    return "P2P " + getID();
  }

  @Override
  public void writeArray(byte[] s) {}

  @Override
  public void writeByte(byte b) {}

  @Override
  public void writeString(String s) {}
}
