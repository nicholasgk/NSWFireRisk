"""
A component which allows you to parse an NSW fire risk feed into a sensor

"""
import asyncio
import re
from xml.dom import minidom
import urllib.request
import logging
import voluptuous as vol
from datetime import timedelta
from dateutil import parser
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME)

__version__ = '0.0.2'
_LOGGER = logging.getLogger(__name__)

CONF_FEED_URL = 'feed_url'
CONF_REGION  = 'region'


DEFAULT_SCAN_INTERVAL = timedelta(hours=1)

COMPONENT_REPO = ''
SCAN_INTERVAL = timedelta(hours=1)
ICON = 'mdi:fire'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_FEED_URL, default='http://www.rfs.nsw.gov.au/feeds/fdrToban.xml'): cv.string,
    vol.Required(CONF_REGION, default=4): cv.positive_int,
})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    async_add_devices([FireRiskSensor(
        feed=config[CONF_FEED_URL],
        name=config[CONF_NAME],
        region=config[CONF_REGION]
        )], True)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


class FireRiskSensor(Entity):
    def __init__(self, feed: str, name: str, region: str):
        self._feed = feed
        self._name = name
        self._region = region
        self._state = None
        self._regionName = None
        self._councils = None
        self._dangerLevelToday = None
        self._dangerLevelTomorrow = None
        self._fireBanToday = None
        self._fireBanTomorrow = None
#         self._entries = []




    def update(self):
        parsedFeed = minidom.parse(urllib.request.urlopen(self._feed))

        if not parsedFeed:
            return False
        else:
            itemlist = parsedFeed.getElementsByTagName('District')
            
            for district in itemlist:
            
                if (int(getText(district.getElementsByTagName('RegionNumber')[0].childNodes)) == int(self._region)):
                    
                    self._state = getText(district.getElementsByTagName('DangerLevelToday')[0].childNodes)
#                     self._entries = []
        
#                     entryValue = {}
                    self._regionName = getText(district.getElementsByTagName('Name')[0].childNodes)
#                     entryValue['RegionNumber'] = getText(district.getElementsByTagName('RegionNumber')[0].childNodes)
                    self._councils = getText(district.getElementsByTagName('Councils')[0].childNodes)
                    self._dangerLevelToday  = getText(district.getElementsByTagName('DangerLevelToday')[0].childNodes)
                    self._dangerLevelTomorrow  = getText(district.getElementsByTagName('DangerLevelTomorrow')[0].childNodes)
                    self._fireBanToday  = getText(district.getElementsByTagName('FireBanToday')[0].childNodes)
                    self._fireBanTomorrow  = getText(district.getElementsByTagName('FireBanTomorrow')[0].childNodes)
#                     self._entries.append(entryValue)
                    continue



    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

#     @property
#     def device_state_attributes(self):
#         return {
#             'entries': self._entries
#         }

    @property
    def regionName(self):
        return self._regionName

    
    @property
    def councils(self):
        return self._councils
    
    @property
    def dangerLevelToday(self):
        return self._dangerLevelToday
    
    @property
    def dangerLevelTomorrow(self):
        return self._dangerLevelTomorrow
    
    @property
    def fireBanToday(self):
        return self._fireBanToday
    
    @property
    def fireBanTomorrow(self):
        return self._fireBanTomorrow
    
