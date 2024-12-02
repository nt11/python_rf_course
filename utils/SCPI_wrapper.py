import logging
import sys
import pyvisa
import pyvisa_py

class SCPIWrapper:
    def __init__(self, instr , log, name = 'SA'):
        self.instr      = instr
        self.log        = log
        self.name       = name


    def write(self, cmd: str):
        if self.instr is not None:
            # Add logging to the write command (Debug Level)
            self.log.debug(f"{self.name}: Write: {cmd}")
            self.instr.write(cmd)
            # Check for errors
            e = self.instr.query('SYST:ERR?').strip().split(',')
            if int(e[0]) != 0:
                self.log.error(f"{self.name}: Error: {e[1]}")

    def query(self, cmd: str):
        if self.instr is not None:
            # Add logging to the query command (Debug Level)
            self.log.debug(f"{self.name}: Query: {cmd}")
            ans = self.instr.query(cmd).strip()
            # Check for errors
            e = self.instr.query('SYST:ERR?').strip().split(',')
            if int(e[0]) != 0:
                self.log.error(f"{self.name} Error: {e[1]}")
            return ans
