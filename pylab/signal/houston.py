import requests


class DDS:
  """
  DDS represents a digital signal synthesizer using the houston web service.
  """

  def __init__(self, id, name, hostname):
    """
    Initializes the DDS to represent the DDS with given name and id.
    """
    self._id = id
    self._name = name
    self._hostname = hostname

  @property
  def id(self):
    """
    Returns the DDS id.
    """
    return self._id

  @property
  def name(self):
    """
    Returns the DDS name.
    """
    return self._name

  @property
  def hostname(self):
    """
    Returns the hostname of the DDS rack.
    """
    return self._hostname

  def update(self, frequency, amplitude=1.0, nodwells=[False, False],
             duration=26.84e-3, interval=26.14e-6):
    """
    Updates the DDS to the given parameter configuration.

    If the frequency or amplitude are floats they will be configured in
    singletone mode. If frequency or amplitude are lists (of length two),
    they will be interpreted as lower and upper digital ramp limits. In the
    case that frequency or amplitude is a numpy array, this will be interpreted
    as data points for memory playback.
    """
    fconfig = {}

    if isinstance(frequency, list):
      fconfig['mode'] = 'sweep'
      fconfig['value'] = 0
      fconfig['limits'] = frequency
    else:
      fconfig['mode'] = 'const'
      fconfig['value'] = frequency
      fconfig['limits'] = [0, 0]

    aconfig = {}
    if isinstance(amplitude, np.ndarray):
      aconfig['mode'] = 'playback'
      aconfig['data'] = np.clip(amplitude[::-1], 0, 1).tolist()
      aconfig['value'] = 1.0
    else:
      aconfig['mode'] = 'const'
      aconfig['value'] = amplitude
      aconfig['data'] = []

    headers = {'Content-Type': 'application/json'}
    payload = {
        'id': self.id,
        'name': self.name,
        'amplitude': {
            'mode': aconfig['mode'],
            'const': {
                'value': aconfig['value'],
            },
            'playback': {
                'trigger': True,
                'duplex': False,
                'interval': interval,
                'data': aconfig['data']
            }
        },
        'phase': {
            'mode': 'const',
            'value': 0
        },
        'frequency': {
            'mode': fconfig['mode'],
            'const': {
                'value': fconfig['value']
            },
            'sweep': {
                'nodwells': nodwells,
                'limits': fconfig['limits'],
                'duration': duration
            }
        }
    }

    response = requests.put(f'http://{self.hostname}/devices/dds/{self.id}',
                            headers=headers, json=payload)
    response.raise_for_status()

    return response
