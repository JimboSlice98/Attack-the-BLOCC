import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_simulation_xml(rows, cols, spacing_x, spacing_y, filename, tx_range, interference_range, success_ratio_tx, success_ratio_rx):
    simconf = ET.Element("simconf", version="2023090101")
    simulation = ET.SubElement(simconf, "simulation")
    
    ET.SubElement(simulation, "title").text = "network_protocol_test"
    ET.SubElement(simulation, "randomseed").text = "generated"
    ET.SubElement(simulation, "motedelay_us").text = "1000000"
    
    radiomedium = ET.SubElement(simulation, "radiomedium")
    radiomedium.text = "org.contikios.cooja.radiomediums.UDGM"
    ET.SubElement(radiomedium, "transmitting_range").text = str(tx_range)
    ET.SubElement(radiomedium, "interference_range").text = str(interference_range)
    ET.SubElement(radiomedium, "success_ratio_tx").text = str(success_ratio_tx)
    ET.SubElement(radiomedium, "success_ratio_rx").text = str(success_ratio_rx)
    
    events = ET.SubElement(simulation, "events")
    ET.SubElement(events, "logoutput").text = "40000"
    
    motetype = ET.SubElement(simulation, "motetype")
    motetype.text = "org.contikios.cooja.contikimote.ContikiMoteType"
    
    ET.SubElement(motetype, "description").text = "Cooja Node"
    ET.SubElement(motetype, "source").text = "[CONFIG_DIR]/udp-p2p.c"
    ET.SubElement(motetype, "commands").text = "$(MAKE) -j$(CPUS) udp-p2p.cooja TARGET=cooja"
    
    interfaces = [
        "org.contikios.cooja.interfaces.Position",
        "org.contikios.cooja.interfaces.Battery",
        "org.contikios.cooja.contikimote.interfaces.ContikiVib",
        "org.contikios.cooja.contikimote.interfaces.ContikiMoteID",
        "org.contikios.cooja.contikimote.interfaces.ContikiRS232",
        "org.contikios.cooja.contikimote.interfaces.ContikiBeeper",
        "org.contikios.cooja.interfaces.IPAddress",
        "org.contikios.cooja.contikimote.interfaces.ContikiRadio",
        "org.contikios.cooja.contikimote.interfaces.ContikiButton",
        "org.contikios.cooja.contikimote.interfaces.ContikiPIR",
        "org.contikios.cooja.contikimote.interfaces.ContikiClock",
        "org.contikios.cooja.contikimote.interfaces.ContikiLED",
        "org.contikios.cooja.contikimote.interfaces.ContikiCFS",
        "org.contikios.cooja.contikimote.interfaces.ContikiEEPROM",
        "org.contikios.cooja.interfaces.Mote2MoteRelations",
        "org.contikios.cooja.interfaces.MoteAttributes"
    ]
    
    for interface in interfaces:
        ET.SubElement(motetype, "moteinterface").text = interface
    
    mote_id = 1
    for i in range(rows):
        for j in range(cols):
            mote = ET.SubElement(motetype, "mote")
            interface_config_pos = ET.SubElement(mote, "interface_config")
            interface_config_pos.text = "org.contikios.cooja.interfaces.Position"
            ET.SubElement(interface_config_pos, "pos", x=str(j * spacing_x), y=str(i * spacing_y))
            
            interface_config_id = ET.SubElement(mote, "interface_config")
            interface_config_id.text = "org.contikios.cooja.contikimote.interfaces.ContikiMoteID"
            ET.SubElement(interface_config_id, "id").text = str(mote_id)
            
            mote_id += 1
    
    pretty_xml = prettify(simconf)
    with open(filename, "w") as f:
        f.write(pretty_xml)

# Generate simulation file
create_simulation_xml(
    rows=5, 
    cols=4, 
    spacing_x=3, 
    spacing_y=12, 
    filename="../simulation-large.csc", 
    tx_range=14, 
    interference_range=20, 
    success_ratio_tx=0.9, 
    success_ratio_rx=0.9
)
