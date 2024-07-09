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

  private static final long TRANSMISSION_DURATION = Simulation.MILLISECOND*5;
  private static final long SEND_INTERVAL = Simulation.MILLISECOND*1000*60 - TRANSMISSION_DURATION;
  private static final long RANDOM_RANGE = Simulation.MILLISECOND*25;
  private static final int LOG_LENGTH = 60;
  private long txCount = 0;
  private Map<String, Long> msgCache = new HashMap<>();

  public Peer2PeerMote(MoteType moteType, Simulation simulation) throws MoteType.MoteTypeCreationException {
    super(moteType, simulation);
  }
  
  protected void execute(long time) {
    System.out.println("Mote " + getID() + " execute() function called");
    if (radio == null) {
      radio = (ApplicationRadio) getInterfaces().getRadio();
      rd = getSimulation().getRandomGenerator();
    }
    schedulePacket();
  }

  @Override
  public void receivedPacket(RadioPacket p) {
    System.out.println(p);
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
        logf(logMsg, "Duplicate");
        return;
      // else if (!withinGrace(timeOfBroadcast)) {
      //   logf(LogMsg, "Out of grace");
      //   return;
      }

      msgCache.put(key, timeOfBroadcast);
      
      // Handle incomming attestations
      if (attestNode != 0 && originNode != getID()) {
        logf(logMsg, "Rebroadcast attestation");
        broadcastMessage(messageNum, originNode, attestNode, timeOfBroadcast);
        return;
      }
      else if (attestNode != 0) {
        logf(logMsg, "Attestation received");
        return;
      }
      
      // Handle incomming messages
      logf(logMsg, "Rebroadcast message");
      broadcastMessage(messageNum, originNode, attestNode, timeOfBroadcast);

      // Create new attestation


    } catch (NumberFormatException e) {
      System.out.println("Mote " + getID() + " received bad data: " + e);
    }
  }

  private void broadcastMessage(long messageNum, int originNode, int attestNode, long timeOfBroadcast) {
    // System.out.println("Mote " + getID() + " scheduling relay message " + getSimulation().getSimulationTimeMillis());

    getSimulation().scheduleEvent(new MoteTimeEvent(this) {
      @Override
      public void execute(long t) {
        // System.out.println("Mote " + getID() + " sending relayed message " + getSimulation().getSimulationTimeMillis());
        String data = messageNum + "|" + originNode + "|" + attestNode + "|" + timeOfBroadcast + "|" + getID();
        radio.startTransmittingPacket(new COOJARadioPacket(data.getBytes(StandardCharsets.UTF_8)), TRANSMISSION_DURATION);
        // System.out.println("Mote " + getID() + " rebroadcasting message " + getSimulation().getSimulationTimeMillis());
      }
    }, getSimulation().getSimulationTime() + (long)(RANDOM_RANGE*rd.nextDouble()));
  }

  @Override
  public void sentPacket(RadioPacket p) {
    // System.out.println("Mote " + getID() + " sentPacket() function called " + getSimulation().getSimulationTimeMillis());
    // schedulePacket();
  }

  private void schedulePacket() {
    // System.out.println("Mote " + getID() + " scheduling message " + txCount + " " + getSimulation().getSimulationTimeMillis());

    getSimulation().scheduleEvent(new MoteTimeEvent(this) {
      @Override
      public void execute(long t) {
        // System.out.println("Mote " + getID() + " sending message " + txCount + " "  + getSimulation().getSimulationTimeMillis());
        String data = txCount + "|" + getID() + "|0";
        long timeOfBroadcast = getSimulation().getSimulationTime();

        radio.startTransmittingPacket(new COOJARadioPacket(
          (data + "|" + timeOfBroadcast + "|" + getID()).getBytes(StandardCharsets.UTF_8)
          ), TRANSMISSION_DURATION);
        
        log("Tx: " + "'" + data + "|" + timeOfBroadcast + "'");
        msgCache.put(data, timeOfBroadcast);
        txCount++;

        schedulePacket();
      }
    }, getSimulation().getSimulationTime() + SEND_INTERVAL + (long)(RANDOM_RANGE*rd.nextDouble()));
  }

  private void logf(String logMsg, String additionalMsg) {
    String logData = String.format("%-" + LOG_LENGTH + "s", logMsg) + " -> " + additionalMsg;
    log(logData);
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