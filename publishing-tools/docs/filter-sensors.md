# Sensor Filter

This tool filters sample lines from stdin to only include sensors in config file passing all sanity checks.

## Usage

```
# process file
filter-sensor config < input.csv

# process stream
sample stream | filter-sensor config
```

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

must have values which pass the specified range check. `BMP180.pressure` will be allowed regardless of value, since we didn't include any sanity checks.
