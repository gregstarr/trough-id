import configparser
import pathlib
import functools
from . import _api


_config_file = pathlib.Path(__file__).parent / "config.ini"
_config = configparser.ConfigParser()
_config.read(_config_file)
tec_dir = _config.get("PATHS", "tec")
trough_dir = _config.get("PATHS", "trough")

get_data = functools.partial(_api.get_data, tec_dir, trough_dir)