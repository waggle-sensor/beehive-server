# Sensor Filter

## Usage

`filter-sensor` filters sample lines from stdin to only include:

* allowed sensors from config file
* values from allowed sensors in config file passing sanity checks

## Config

The config file is a JSON file format oraganized as follows:

```json
{
  "sensor 1": {
    "check 1": "params 1",
    "check 2": "params 2",
    ...
  },
  "sensor 2": {
    "check 1": "params 1",
    "check 2": "params 2",
    ...
  },
  ...
}
```

The top level keys specify the allowed sensors. Only these will be considered as output. For example:

```json
{
  "HTU21D.humidity": {
    "range": [-1, 101]
  },
  "HTU21D.temperature": {
    "range": [-40, 50]
  },
  "BMP180.temperature": {
    "range": [-40, 50]
  },
  "BMP180.pressure": {
  },
}
```

In this case, the following sensors will be considered:
```
HTU21D.humidity
HTU21D.temperature
BMP180.temperature
BMP180.pressure
```

In addition, these sensors

```
HTU21D.humidity
HTU21D.temperature
BMP180.temperature
```

must have values which pass the specified range check.
