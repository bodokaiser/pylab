import numpy as np

from pylab import Device


class DS1000(Device):
  """
  DS1000 represents an oscilloscope of the DS1000 series from Rigol.
  """

  def __init__(self, hostname, timeout=5000):
    """
    Initializes the device and unlocks the front panel input.
    """
    super().__init__(hostname, timeout)

    # by default the scope will lock its front panel input
    self.unlock()

  def run(self):
    """
    Puts the scope into RUN mode.
    """
    return self.resource.write(':RUN')

  def single(self):
    """
    Puts the scope into SINGLE mode.
    """
    return self.resource.write(':SINGle')

  def lock(self):
    """
    Locks to the front panel input.
    """
    return self.resource.write(':KEY:LOCK ENABle')

  def unlock(self):
    """
    Unlocks the front panel input.
    """
    return self.resource.write(':KEY:LOCK DISable')

  def measure(self, param, channel):
    """
    Returns the measurement value of the specified parameter.
    """
    self.resource.write(f':MEASure:{param}? CHANnel{channel}')[0]

    return float(self.resource.read())
    # using this will let the connection die very fast...
    # return self.resource.query_ascii_values(f':MEASure:{param}? CHANnel{channel}')[0]

  def measure_mean_voltage(self, channel=1):
    """
    Returns the average voltage measured.
    """
    return self.measure('VAVerage', channel)

  def measure_rms_voltage(self, channel=1):
    """
    Returns the root means squared voltage measured.
    """
    return self.measure('VRMS', channel)

  def measure_min_voltage(self, channel=1):
    """
    Returns the minimum voltage measured.
    """
    return self.measure('VMIN', channel)

  def measure_max_voltage(self, channel=1):
    """
    Returns the maximum voltage measured.
    """
    return self.measure('VMAX', channel)
