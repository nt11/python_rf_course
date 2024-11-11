class PA():
    def __init__(self, serial: str) -> None:
        """
        Initialize class. Read from a data file the curves of an amplifier
        :param serial: The serial of the PA
        """

        # Read the file (page 1-83, 1-84 example 008)

        # Split the data into lines using the split("\n") method (look at page 1-122, example 022)

        # Ignore first line using slicing [1:] (look at page 1-100, 1-101 example 010)

        # Loop through the lines (look at page 1-106, example 013)

            # Split each line into fields using the split(",") method (look at page 1-122, example 022)

            # Extract the pin, pout, and frequency cast into integer (frequency) and float (pin, pout) - int(x) and float(x)

            # Compute the gain by subtracting pout - pin

            # Check if the frequency is not in the dictionary - if f not in self.measurements.keys()

                # If not, initialize the dictionary entry to an empty list - self.measurements[f] = []

            # Add the data to the dictionary - self.measurements[f].append({'pin': ..., 'pout': ..., 'gain': ...})

        pass

    def compute_small_signal_gain(self, f: int, N: int = 5) -> float:
        """
        Computes the small signal gain for an amplifier at a frequency
        :param f: Frequency
        :param N: Number of points to use in the calculation
        :return:
        """

        # Check if the frequency is in the dictionary

        # Initialize the gain sum

        # Loop through the first N entries of the frequency

            # Add the gain to the sum

        # Return the average gain

        pass

    def compute_output_p1db(self, f: int) -> float:
        """
        Computes the P1dB for an amplifier at a frequency

        :param f: Frequency to check
        :return: Output P1dB if found, None otherwise
        """

        # Check if the frequency is in the dictionary

        # Loop through the entries of the frequency

            # Check if the gain is 1 dB below the small signal gain

                # Return the output power

        # If frequency or P1dB weren't found return None
        pass


if __name__ == "__main__":
    serials = ['SN1234', 'SN2222', 'SN3333', 'SN4321', 'SN4444']
    db = []
    for ser in serials:
        db.append(PA(ser))

    # print all P1dBs

    for pa in db:
        print(f"Serial number {pa.serial}:")
        print("--------------------------")
        for f in pa.measurements:
            print(f"Frequency = {f}, Small signal gain = {pa.compute_small_signal_gain(f):.2f} OP1dB = {pa.compute_output_p1db(f):.2f}")
        print("\n")
