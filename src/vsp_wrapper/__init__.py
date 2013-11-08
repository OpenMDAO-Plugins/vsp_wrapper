"""
File-based wrapper for VSP 1.7.1

At startup it reads a VSP XML file into component variables.
When run, the component variables are written to another VSP XML file
and then VSP is run in batch mode.
"""

from __future__ import absolute_import

from .wrapper import VSP
from .parageom import VSPParametricGeometry, VSPSender

