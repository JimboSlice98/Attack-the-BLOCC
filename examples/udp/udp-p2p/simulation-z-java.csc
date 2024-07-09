<?xml version="1.0" ?>
<simconf version="2023090101">
  <simulation>
    <title>My simulation</title>
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
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>1</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="0" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>2</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="3" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>3</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="6" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>4</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="9" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>5</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="12" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>6</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="15" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>7</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="18" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>8</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="21" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>9</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="24" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>10</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="27" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>11</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="30" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>12</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="33" y="0"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>13</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="0" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>14</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="3" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>15</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="6" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>16</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="9" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>17</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="12" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>18</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="15" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>19</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="18" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>20</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="21" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>21</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="24" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>22</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="27" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>23</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="30" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>24</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="33" y="12"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>25</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="0" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>26</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="3" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>27</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="6" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>28</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="9" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>29</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="12" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>30</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="15" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>31</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="18" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>32</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="21" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>33</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="24" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>34</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="27" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>35</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="30" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>36</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="33" y="24"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>37</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="0" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>38</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="3" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>39</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="6" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>40</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="9" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>41</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="12" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>42</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="15" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>43</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="18" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>44</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="21" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>45</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="24" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>46</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="27" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>47</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="30" y="36"/>
        </interface_config>
      </mote>
      <mote>
        <interface_config>
          org.contikios.cooja.motes.AbstractApplicationMoteType$SimpleMoteID
          <id>48</id>
        </interface_config>
        <interface_config>
          org.contikios.cooja.interfaces.Position
          <pos x="33" y="36"/>
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
    <bounds x="400" y="160" height="868" width="1320" z="1"/>
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
    <bounds x="843" y="74" height="700" width="600"/>
  </plugin>
</simconf>
