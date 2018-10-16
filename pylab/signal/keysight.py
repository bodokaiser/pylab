from pylab import Device


class FG33250(Device):
  """
  FG33250 represents the 33250 function generator from Keysight.
  """

  def width(self, value, channel):
    """
    Sets the width of the output pulse.
    """
    self.resource.write(f':PULS{channel}:WIDTH {value:1.11f}')
