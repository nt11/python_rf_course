import pyvisa
import pyvisa-py # Alternatively install NI drivers

rm = pyvisa.ResourceManager()

try:
    # Connect to instrument
    instr = rm.open_resource('TCPIP::192.168.1.100::INSTR')
    instr.timeout = 5000

    # Basic IEEE-488.2 commands
    idn = instr.query('*IDN?')  # Get ID
    manufacturer, model, serial, firmware = idn.strip().split(',')

    print(f"Manufacturer: {manufacturer}")
    print(f"Model: {model}")
    print(f"Serial Number: {serial}")
    print(f"Firmware Version: {firmware}")

    instr.write('*RST')  # Reset to default
    instr.write('*CLS')  # Clear status

