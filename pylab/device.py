import visa

rm = visa.ResourceManager('@py')


class Device:
  """
  Device represents an arbitrary network device connectred through the VISA.
  """

  def __init__(self, hostname: str, timeout: int = 5000) -> None:
    """
    Initializes a device by openning a visa connection.
    """
    self.resource = rm.open_resource(f'TCPIP0::{hostname}::inst0::INSTR')
    self.resource.timeout = timeout

  def holla(self) -> str:
    """
    Returns the identifier of the device.
    """
    return self.resource.query('*IDN?')

  def close(self) -> None:
    """
    Closes the underlaying connection.
    """
    self.resource.close()
