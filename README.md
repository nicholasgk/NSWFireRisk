# NSWFireRisk
A custom component for [Home Assistant](https://www.home-assistant.io/) which gives the current fire risk for a NSW region.

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE.md)

![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]


To get started put `/custom_components/firerisk/` here:
`<config directory>/custom_components/firerisk/`

**Example configuration.yaml:**

```yaml
sensor:
  platform: firerisk
  name: NSW Fire Risk
  region: 4
```

**Configuration variables:**

key | description
:--- | :---
**platform (Required)** | The platform name
**name (Required)** | Name your Sensor
**region (Required)** | The region number of the data to read back - https://www.rfs.nsw.gov.au/fire-information/fdr-and-tobans
**feed_url (Optional)** | The xml feed URL **Default** `http://www.rfs.nsw.gov.au/feeds/fdrToban.xml`


***


Due to how `custom_components` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.
