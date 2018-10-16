import numpy as np

from pylab import Device


class MSOX6000(Device):
  """
  MSOX6000 represents an oscilloscope of the Keysight MSOX6000 series.
  """

  def __init__(self, hostname, timeout=5000):
    """
    Initializes the device.
    """
    super().__init__(hostname, timeout)

  def single(self):
    """
    Puts scope into single mode.
    """
    return self.resource.write(':SINGle')

  def save(self, filename):
    """
    Saves current waveform data to attached usb drive in HDF5 format.
    """
    return self.resource.write(f':SAVE:WMEMory:STARt "\\usb\\{filename}.h5"')

  def data(self, channel=1):
    """
    Fetches the waveform data through the network and returns time and voltages
    as numpy arrray.

    To have waveform data available, you need to put the scope into SINGLE
    mode and apply an (external) trigger signal.
    """
    self.resource.write(':WAVeform:FORMat WORD')
    self.resource.write(':WAVeform:BYTeorder LSBFirst')
    self.resource.write(':WAVeform:UNSigned 0')
    self.resource.write(f':WAVeform:SOURce CHANnel{channel}')

    values = self.resource.query_binary_values(
        ':WAVeform:DATA?', datatype='h', container=np.array, header_fmt='ieee')

    xorg = self.resource.query_ascii_values(':WAVeform:XORigin?')[0]
    xinc = self.resource.query_ascii_values(':WAVeform:XINcrement?')[0]
    yorg = self.resource.query_ascii_values(':WAVeform:YORigin?')[0]
    yinc = self.resource.query_ascii_values(':WAVeform:YINcrement?')[0]
    yref = self.resource.query_ascii_values(':WAVeform:YREference?')[0]

    U = yorg + yinc * (values - yref)
    t = xorg + xinc * np.arange(0, len(U))

    return t, U
