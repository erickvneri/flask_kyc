# MIT License
#
# Copyright (c) 2022 erickvneri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
from os import getenv
from configparser import ConfigParser

# Collect environment varlable
__ENV__ = getenv("ENV") or "dev"

# Build TOML parser
config = ConfigParser()
config.read("config.ini")

# Initialize logger
logging.basicConfig(
  format="%(asctime)s - %(levelname)s - %(message)s",
  level=logging.INFO)


class env:
    """
    Application config wrapper
    collecting ConfigParser TOML
    output.
    """
    HOST = config.get(__ENV__, "host")
    PORT = config.getint(__ENV__, "port")
    DB_NAME = config.get(__ENV__, "db_name")
    DB_USER = config.get(__ENV__, "db_user")
    DB_PASSWORD = config.get(__ENV__, "db_password")
    DB_HOST = config.get(__ENV__, "db_host")
    DB_PORT = config.getint(__ENV__, "db_port")
