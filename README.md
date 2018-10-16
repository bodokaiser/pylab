# pylab

Library to connect with laboratory equipement, i.e. oscilloscopes and
signal synthesizers.

## Install

Clone the repository:

```shell
git clone https://github.com/bodokaiser/pylab
```

## Example

Connection with a Rigol DS1000 series oscilloscope:

```python
from pylab.scope import DS1000

scope = DS1000('192.168.1.20')
scope.measure('vavg')
```

Consult the code documentation for details.
