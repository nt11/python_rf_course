from threading import Thread

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
    progress = pyqtSignal(int)
    data = pyqtSignal(np.ndarray, np.ndarray)
    log = pyqtSignal(str)



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
        self.log.emit(f'Thread: Theread start')

        # Set RF output on
        self.scpi_sg.write(":OUTPUT:STATE ON")
        self.scpi_sg.write(":OUTPUT:MOD:STATE OFF")
        #EX5_thread3: Set the SA RBW to 0.1 MHz and the detector to average using the SCPI wrapper(slide 2-55)
        self.scpi_sa.write(":Sense:band:res 0.1 MHz")
        self.scpi_sa.write(":sense:detector AVER")


        # Trace Clear/write mode
        self.scpi_sa.write("TRACe:MODE WRITe")
        self.scpi_sa.write("INITiate:CONTinuous OFF")

        # Create a list to store the scan data
        power = np.array([])
        freq  = np.array([])
        for i, f in enumerate(self.f_scan):
            # Set the SG to the frequency of the current scan point
            self.scpi_sg.write(f"freq {f} MHz")
            # Set the SA center frequency
            self.scpi_sa.write(f"sense:FREQuency:CENTer {f} MHz")
            # Set the span
            self.scpi_sa.write(f"sense:FREQuency:SPAN 5 MHz")
            # Initiate a single sweep
            self.scpi_sa.write("INITiate:IMMediate")
            try:
                self.scpi_sa.query("*OPC?")
            except pyvisa.errors.VisaIOError:
                self.log.emit(f"Thread: OPC Failed at {f} MHz")

            #EX5_thread4: Set marker to peak - Use SCPI Wrapper, use SCPI commands from the auxiliary sheet
            self.scpi_sa.write(':calc:mark:max')


            #EX5_thread5: Get the peak_value by quering the SCPI Wrapper. Use SCPI commands from the auxiliary sheet
            #Remember to strip the output and cast to float
            peak_value =float(self.scpi_sa.query(':calc:mark1:Y?'))
            # Set the reference level

            max_level  = np.ceil( peak_value/10 + 1)*10
            set_level  = float(self.scpi_sa.query(f"DISP:WIND:TRAC:Y:RLEV?").strip() )
            if set_level != max_level:
                self.log.emit(f"Thread: Setting reference level to {max_level}")
                self.scpi_sa.write(f"DISP:WIND:TRAC:Y:RLEV {max_level}")
            # save the peak value and frequency
            power = np.append(power, peak_value)
            freq  = np.append(freq, f)

            #EX5_thread4: Emit the frequency and power every 20 iterations (slide 4-27, example o310)
            if i in range(0,len(self.f_scan),20):
                self.data.emit(freq, power)


            #EX5_thread5: Emit the progress signal (slide 4-27, example o310) - scale the progress to a maximum of 100
            self.progress.emit(i/len(self.f_scan)*100)


            if not self.running:
                break

        #EX5_thread6: Emit the final freq,power  (slide 4-27, example o310)
        self.data.emit(freq,power)


    def stop(self):
        self.running = False

