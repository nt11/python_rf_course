from PyQt6.QtCore       import QThread, pyqtSignal
import numpy as np


class LongProcess(QThread):
    #EX5_thread_1:  Define signals as class attributes (slide 4-27 example o310)
    #Define the following signals:
    # progress (sends an integer)
    # data (sends two numpy arrays - np.ndarray)
    # log (sends a string)
    #
    #
    #

    def __init__(self, f_scan,scpi_sa, scpi_sg):
        super().__init__()
        self.f_scan     = f_scan
        self.scpi_sa    = scpi_sa
        self.scpi_sg    = scpi_sg
        
        self.running    = False

    def run(self):
        # Save the instrument attributes for recall at the end of the scan
        self.running = True
        #EX5_thread2: Send a log message that you are starting the scan (Start with the word "Thread:")
        #

        # EX5_thread3: Set the SG output to ON and the modulation to OFF using the SCPI wrapper. Use the auxiliary sheet for the SCPI commands
        #
        #
        #EX5_thread4: Set the SA RBW to 0.1 MHz and the detector to average, trace mode to write and single sweep mode
        # using auxiliary sheet for SCPI commands
        #
        #
        #
        #

        # Create a list to store the scan data
        power = np.array([])
        freq  = np.array([])
        for i, f in enumerate(self.f_scan):
            #EX5_thread5 Set the SG to the frequency of the current scan point using auxiliary sheet for SCPI commands
            #
            #EX5_thread6: Set the SA center frequency to the current scan point using auxiliary sheet for SCPI commands
            #
            #EX5_thread7: Set the SA span to 5MHz using auxiliary sheet for SCPI commands
            #
            #EX5_thread8: Initiate a single sweep using auxiliary sheet for SCPI commands
            #
            try:
            #EX5_thread9: Check for operation complete using the SCPI wrapper. Slide 4-8
            #
            except pyvisa.errors.VisaIOError:
                self.log.emit(f"Thread: OPC Failed at {f} MHz")

            #EX5_thread10: Set marker to peak - Use SCPI Wrapper, use SCPI commands from the auxiliary sheet
            #
            #EX5_thread11: Get the peak_value by quering the SCPI Wrapper. Use SCPI commands from the auxiliary sheet
            #Remember to strip the output and cast to float
            #peak_value =
            # Set the reference level
            max_level  = np.ceil( peak_value/10 + 1)*10
            #EX5_thread12: Get the current reference level using the SCPI wrapper. Remember to strip and cast to float
            #set_level  =
            #EX6_thread13: If the set_level is not equal to the max_level, set the reference level to max_level and emit
            # a log message to say you have set the reference level. Use SCPI commands from the auxiliary sheet
            #
            #
            #
            # save the peak value and frequency
            power = np.append(power, peak_value)
            freq  = np.append(freq, f)

            #EX5_thread14: Emit the frequency and power every 20 iterations (slide 4-27, example o310)
            #
            #

            #EX5_thread15: Emit the progress signal (slide 4-27, example o310) - scale the progress to a maximum of 100
            #

            if not self.running:
                break

        #EX5_thread16: Emit the final freq,power  (slide 4-27, example o310)
        #


    def stop(self):
        self.running = False

