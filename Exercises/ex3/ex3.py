
# import sys, pyvisa, time, numpy (example 105), matplotlib (slide 2-39)

def read_trace_find_max(sa):
    # Query the instrument for the trace data (see slide 2-58)

    # Read the ASCII data (same as slide 2-58)

    # Convert the string data to a numpy array (same as slide 2-58)

    # Get the current frequency settings (slide 2-56)
    #start_freq  = ...
    #stop_freq   = ...
    #num_points  = ... # convert the setting in slide 2-55 into a query command

    # Calculate frequency points, use np.linspace (slide 2-36)
    #f = ...

    # Plot the data (slide 2-39- 2-40), use plot, xlabel, ylabel, title,grid ('on'), show

    # Use np.argmax to find the maximum value of the trace (slide 2-36) to find f_peak (the frequency) and y_peak (the power)

    return f_peak, y_peak

if __name__ == "__main__":
    # Make matplot lib interactive (need to change the settings like in slide 2-44 - 2-47, otherwise plots will disappear)
    import matplotlib
    matplotlib.use('TkAgg')
    plt.ion()


    # Connect to the instrument (slide 2-54)
    # rm = ...
    try:

        #ip = ...
        #sa = ...

        # Query the signal generator name (slide 2-54)

    except pyvisa.errors.VisaIOError:
        print(f'Failed to connect to the instrument at {ip}')
        sys.exit(1)

    # Reset and clear all status (errors) of the spectrum analyzer (slide 2-54)

    #reset
    #cls

    # Set the spectrum analyzer to maximal span (*)
    sa.write("sense:FREQuency:SPAN:FULL")
    # Set auto resolution bandwidth (*)
    sa.write("sense:BANDwidth:RESolution:AUTO ON")

    # Set the trace to clear/write (slide 2-55)
    #sa.write ...

    # Set the sweep mode to continues (*)
    sa.write("INITiate:CONTinuous ON")

    # Wait for the sweep to complete
    # sleep for 2 seconds (slide 2-15)

    # Find the peaks and plot by calling the read_trace_find_max function
    # Fc,p = ...

    # Set the refrence level to the maximum. Compute a desired max level (slightly above the maximum peak) and set it
    # slide 2-56
    #max_level = ...
    #sa.write ...


    # Set the span to 100:10:1:0.1:0.01 MHz (*)
    Fspan = np.logspace(2, -2, 5) # Span in MHz

    # Loop over the spans
        # set the center frequency to the peak frequency and the span to the current span (slide 2-55)
        #sa.write ...
        #sa.write ...

        # sleep for 2 seconds (slide 2-15)

        # Find the peaks and plot by calling the read_trace_find_max function
        #Fc,p = ...

        # print the center frequency, span and peak power (using f-string slide 1-128, 1-129)

        #print(...)

    # Out of the loop...
    # print the last RBW

    # Close the connection (side 2-57, example 110)
    #sa....
    #rm...


        
