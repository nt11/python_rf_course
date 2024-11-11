class PA():
    def __init__(self, serial: str) -> None:
        """
        Initialize class. Read from a data file the curves of an amplifier
        :param serial: The serial of the PA
        """
        pass

    def compute_small_signal_gain(self, f: int, N: int = 5) -> float:
        """
        Computes the small signal gain for an amplifier at a frequency
        :param f: Frequency
        :param N: Number of points to use in the calculation
        :return:
        """
        pass

    def compute_output_p1db(self, f: int) -> float:
        """
        Computes the P1dB for an amplifier at a frequency

        :param f: Frequency to check
        :return: Output P1dB if found, None otherwise
        """
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
