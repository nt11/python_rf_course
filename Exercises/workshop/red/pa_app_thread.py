#WKR_1: Import the necessary modules
#...
from os import write


class PaScan(QThread):
    # Define signals as class attributes (for progressbar and returned data)
    progress    = pyqtSignal(int)
    data        = pyqtSignal(np.ndarray, np.ndarray, bool, str, str) # freq, power, clf , legend, color
    log         = pyqtSignal(str)
    # LCD signals
    #WKR_2: Define the LCD signals
    #lcd_g      = ...
    #lcd_op1dB  = ...
    #lcd_oip3   = ...
    #lcd_oip5   = ...
    lcd_g = pyqtSignal(float)
    lcd_op1dB = pyqtSignal(float)
    lcd_oip3 = pyqtSignal(float)
    lcd_oip5 = pyqtSignal(float)



    def __init__(self, f_scan,scpi_sa, scpi_sg, loss = 0):
        super().__init__()
        self.f_scan     = f_scan
        self.scpi_sa    = scpi_sa
        self.scpi_sg    = scpi_sg
        self.loss       = loss
        
        self.running    = False

    def run(self):
        # Save the instrument attributes for recall at the end of the scan
        self.running = True
        self.log.emit("Thread: Starting scan")

        #WK_1: Signal Generator RF Output On
        #
        self.scpi_sg.write("OUTP ON")

        #WK_2: Spectrum Analyzer Detector Average, Trace Mode Write, Single Sweep Mode
        #
        #
        #
        self.scpi_sa.write("Det:Aver:Type AVER")
        self.scpi_sa.write("TRAC:MODE WRIT")
        self.scpi_sa.write("INIT:CONT OFF")

        #WK_3: Get the power level from the signal generator into p_tx_nominal
        #p_tx_nominal = ...
        p_tx_nominal = float(self.scpi_sg.query("POW:LEV?"))
        # Create a list to store the scan data
        gain    = np.array([])
        op1dB   = np.array([])
        oip3    = np.array([])
        oip5    = np.array([])

        freq    = np.array([])
        #WKR_3: Loop over the scan frequencies, generate both index i and frequency f
        #for ...
        for i, f in enumerate(self.f_scan):
            # Set the SG to the frequency of the current scan point and power level
            p_tx = p_tx_nominal - 5 # Check gain at low power
            #WK_4: Set the signal generator frequency and power level
            #
            #
            self.scpi_sg.write("freq:cent " + str(f) + "MHz")
            self.scpi_sg.write("POW:LEV " + str(p_tx) + "dBm")
            #WK_5: Set the SA center frequency
            #
            self.scpi_sa.write("FREQ:CENT " + str(f) + "MHz")
            # Small signal gain
            #WK_6: Set the signal generator modulation off for CW testing
            self.scpi_sg.write("MOD:STAT OFF")

            # Get the peak value
            peak_value = self.sa_sweep_marker_max()

            # Set the reference level
            max_level  = np.ceil( peak_value/10 + 1)*10
            set_level  = float(self.scpi_sa.query(f"DISP:WIND:TRAC:Y:RLEV?") )
            if set_level != max_level:
                self.log.emit(f"Thread: Setting reference level to {max_level}")
                self.scpi_sa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")

            # compute the gain and save the frequency and gain
            #WK_7: Compute the gain from the peak value, loss and power level
            #gain_i = ...
            gain_i= peak_value + self.loss-p_tx
            gain = np.append(gain, gain_i)
            freq  = np.append(freq, f)
            # Update the Gain LCD
            #WK_8 Emit a signal to the gain LCD (slide 4-27, example o310)
            #
            self.lcd_g.emit(gain_i)

            # OP1dB
            # Slow scan increase power by 0.1 dB Gheck the gain drop until it is 1 dB
            for p_tx in np.arange(p_tx_nominal - 3, p_tx_nominal + 5, 0.1):
                #WK_9: Set the signal generator power level to p_tx
                #
                self.scpi_sg.write("POW:LEV " + str(p_tx) + "dBm")

                peak_value  = self.sa_sweep_marker_max()
                #WK_10: Compute the gain from the peak value, loss and power level
                #gain_i      = ...
                gain_i = peak_value + self.loss - p_tx
                gain_diff   = gain[-1] - gain_i
                # Check if the gain has dropped by 1 dB
                if gain_diff >= 1:
                    #WK_11 compute the op1dB from the peak value and loss
                    #op1dB_i = ...
                    op1dB_i= peak_value + self.loss
                    #WK_12: Append the op1dB_i to the op1dB list
                    #op1dB = ...
                    op1dB = np.append(op1dB, op1dB_i)

                    #WK_13: Emit a signal to the OP1dB LCD, (slide 4-27, example o310)
                    #
                    self.lcd_op1dB.emit(op1dB_i)
                    break
            else:
                op1dB_i = peak_value + self.loss
                op1dB   = np.append(op1dB, op1dB_i)
                self.lcd_op1dB.emit(op1dB_i)

            # OIP3 and OIP5
            # WK_14 Modulation On and tx power to p_tx_nominal on signal generator
            #
            #
            self.scpi_sg.write("MOD:STAT ON")
            self.scpi_sg.write("POW:LEV " + str(p_tx_nominal) + "dBm")

            peak_value = self.sa_sweep_marker_max()
            p_i        = peak_value + self.loss
            # Next peak twice (OIP3)
            self.scpi_sa.write("CALCulate:MARKer:MAXimum:NEXT")
            self.scpi_sa.write("CALCulate:MARKer:MAXimum:NEXT")
            # Get the peak value
            # WK_15: Get the peak value from the spectrum analyzer using a SCPI command
            #peak_value = ...
            peak_value = self.sa_sweep_marker_max()

            p_i3        = peak_value + self.loss
            # Next peak twice (OIP5)
            self.scpi_sa.write("CALCulate:MARKer:MAXimum:NEXT")
            self.scpi_sa.write("CALCulate:MARKer:MAXimum:NEXT")
            # Get the peak value
            # WK_16: Get the peak value from the spectrum analyzer using a SCPI command
            #peak_value = ...
            peak_value = self.sa_sweep_marker_max()
            p_i5        = peak_value + self.loss

            #WKR_4: Compute the OIP3 (p_i is the fundamental power, p_i3 is the 3rd order power)
            #oip3_i = ...
            oip3_i= p_i + (p_i - p_i3)/2




            oip5_i = p_i + (p_i - p_i5)/4
            oip3 = np.append(oip3, oip3_i)
            oip5 = np.append(oip5, oip5_i)
            self.lcd_oip3.emit(oip3_i)
            self.lcd_oip5.emit(oip5_i)

            # if i%10==0:
            #WKR_5: Emit the data to the plot widget. emit the gain, op1dB, oip3 and oip5.
            #clear the plot for the first call and don't clear for the rest
            #
            #
            #
            #
            if i=0:
                clf=True
            # freq, power, clf , legend, color
            self.data.emit(freq, gain, clf, "Gain", "r")
            self.lcd_op1dB.emit(op1dB_i)
            self.lcd_oip3.emit(oip3_i)
            self.lcd_oip5.emit(oip5_i)
            self.lcd_g.emit(gain_i)






            # Update the progress bar
            self.progress.emit(100 * (i + 1) // len(self.f_scan))
            if not self.running:
                break


    def sa_sweep_marker_max(self):
        # WK_17 Initiate a single sweep on the spectrum analyzer using a SCPI command
        #
        self.scpi_sa.write("INIT")
        try:
        # WK_18 Check for operation complete using a SCPI command (OPC)
            #
            self.scpi_sa.query("*OPC?")
        except pyvisa.errors.VisaIOError:
            self.log.emit(f"Thread: OPC Failed at {f} MHz")
        # Set marker to peak using a SCPI command
        #
        self.scpi_sa.write("CALC:MARK:MAX")
        # Get the peak value
        #peak_value = ...
        peak_value = float(self.scpi_sa.query("CALC:MARK:Y?"))

        return peak_value


    def stop(self):
        self.running = False

