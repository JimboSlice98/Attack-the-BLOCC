<?xml version="1.0" encoding="UTF-8"?>
<simconf version="2023090101">
  <simulation>
    <title>My simulation</title>
    <randomseed>generated</randomseed>
    <motedelay_us>1000000</motedelay_us>
    <radiomedium>
      org.contikios.cooja.radiomediums.UDGM
      <transmitting_range>50.0</transmitting_range>
      <interference_range>100.0</interference_range>
      <success_ratio_tx>1.0</success_ratio_tx>
      <success_ratio_rx>1.0</success_ratio_rx>
    </radiomedium>
    <events>
      <logoutput>40000</logoutput>
    </events>
    <motetype>
      org.contikios.cooja.motes.ImportAppMoteType
      <identifier>apptype64829377</identifier>
      <description>Java Mote</description>
      <motepath>[COOJA_DIR]/build/classes/java/main</motepath>
      <moteclass>org.contikios.cooja.motes.Peer2PeerMote</moteclass>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>1</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="84.17299981169464" y="6.7857008362724125" />
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>2</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="49.9643434812629" y="13.357221927094653" />
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>3</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="21.061121189579794" y="35.99133010618381" />
        </interface_config>
      </mote>
    </motetype>
  </simulation>
  <plugin>
    org.contikios.cooja.plugins.Visualizer
    <plugin_config>
      <moterelations>true</moterelations>
      <skin>org.contikios.cooja.plugins.skins.IDVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.GridVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.TrafficVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.UDGMVisualizerSkin</skin>
      <viewport>4.88544704914079 0.0 0.0 4.88544704914079 -54.14192546656379 118.19272539077168</viewport>
    </plugin_config>
    <bounds x="1" y="1" height="400" width="400" z="2" />
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.LogListener
    <plugin_config>
      <filter />
      <formatted_time />
      <coloring />
    </plugin_config>
    <bounds x="400" y="160" height="868" width="1320" z="1" />
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.TimeLine
    <plugin_config>
      <mote>0</mote>
      <mote>1</mote>
      <mote>2</mote>
      <showRadioRXTX />
      <showRadioHW />
      <showLEDs />
      <zoomfactor>500.0</zoomfactor>
    </plugin_config>
    <bounds x="0" y="1859" height="166" width="1720" z="4" />
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Notes
    <plugin_config>
      <notes>Enter notes here</notes>
      <decorations>true</decorations>
    </plugin_config>
    <bounds x="400" y="0" height="160" width="1320" z="3" />
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.ScriptRunner
    <plugin_config>
      <scriptfile>[COOJA_DIR]/headless_logger.js</scriptfile>
      <active>true</active>
    </plugin_config>
    <bounds x="843" y="74" height="700" width="600" />
  </plugin>
</simconf>
