<?xml version="1.0" ?>
<simconf version="2023090101">
  <simulation>
    <title>java_4x3x1</title>
    <randomseed>generated</randomseed>
    <motedelay_us>1000000</motedelay_us>
    <radiomedium>
      org.contikios.cooja.radiomediums.UDGM
      <transmitting_range>14</transmitting_range>
      <interference_range>20</interference_range>
      <success_ratio_tx>0.9</success_ratio_tx>
      <success_ratio_rx>0.9</success_ratio_rx>
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
      <moteinterface>org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>1</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="0" y="0" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>2</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="3" y="0" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>3</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="6" y="0" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>4</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="0" y="12" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>5</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="3" y="12" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>6</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="6" y="12" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>7</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="0" y="24" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>8</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="3" y="24" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>9</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="6" y="24" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>10</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="0" y="36" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>11</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="3" y="36" z="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>12</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="6" y="36" z="0"/>
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
    <bounds x="1" y="1" height="400" width="400" z="2"/>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.LogListener
    <plugin_config>
      <filter/>
      <formatted_time/>
      <coloring/>
    </plugin_config>
    <bounds x="400" y="160" height="900" width="1320" z="1"/>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.TimeLine
    <plugin_config>
      <mote>0</mote>
      <mote>1</mote>
      <mote>2</mote>
      <showRadioRXTX/>
      <showRadioHW/>
      <showLEDs/>
      <zoomfactor>500.0</zoomfactor>
    </plugin_config>
    <bounds x="0" y="1859" height="166" width="1720" z="4"/>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Notes
    <plugin_config>
      <notes>Enter notes here</notes>
      <decorations>true</decorations>
    </plugin_config>
    <bounds x="400" y="0" height="160" width="1320" z="3"/>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.ScriptRunner
    <plugin_config>
      <scriptfile>[COOJA_DIR]/headless_logger.js</scriptfile>
      <active>true</active>
    </plugin_config>
    <bounds x="400" y="1060" height="700" width="1320"/>
  </plugin>
</simconf>
