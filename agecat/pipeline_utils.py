#############
## LOGGING ##
#############

import logging
from astrobase import log_sub, log_fmt, log_date_fmt

DEBUG = False
if DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO
LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=level,
    style=log_sub,
    format=log_fmt,
    datefmt=log_date_fmt,
)

LOGDEBUG = LOGGER.debug
LOGINFO = LOGGER.info
LOGWARNING = LOGGER.warning
LOGERROR = LOGGER.error
LOGEXCEPTION = LOGGER.exception

#############
## IMPORTS ##
#############

import os
import configparser

def save_status(status_file, section, state_vars):
    """
    Save pipeline status
    Args:
        status_file (string): name of output file
        section (string): name of section to write
        state_vars (dict): dictionary of all options to populate the specified
        section
    """

    config = configparser.RawConfigParser()

    if os.path.isfile(status_file):
        config.read(status_file)

    if not config.has_section(section):
        config.add_section(section)

    for key, val in state_vars.items():
        config.set(section, key, val)

    with open(status_file, 'w') as f:
        config.write(f)

    LOGINFO(f'Saved status for section {section} at {status_file}.')


def load_status(status_file):
    """
    Load pipeline status
    Args:
        status_file (string): name of configparser file
    Returns:
        configparser.RawConfigParser
    """

    config = configparser.RawConfigParser()
    gl = config.read(status_file)

    LOGINFO(f'Reading in {status_file}.')

    return config
