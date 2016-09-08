import re


def parse_sensor_table(text):
    types = {
        'uint24': '4',
        'int24': '5',
    }

    spec = {}

    for chunk in re.split('\n\n+', text.strip()):
        lines = chunk.splitlines()

        sensor_id = int(lines[0].strip(), 16)
        sensor_name = lines[1].strip()
        fields = [tuple(map(str.strip, line.split(':'))) for line in lines[2:]]

        fmts = ''.join(fmt.strip() for _, fmt in fields)
        keys = [key.strip().lower() for key, _ in fields]

        spec[sensor_id] = (sensor_name, fmts, keys)

    return spec


spec = parse_sensor_table('''
00
Board MAC
MAC Address : 3

01
TMP112
Temperature : 6

02
HTU21D
Temperature : 6
Humidity : 6

03
HIH4030
Humidity : 1

04
BMP180
Temperature : 6
Pressure : 4

05
PR103J2
Temperature : 1

06
TSL250RD
Light : 1

07
MMA8452Q
Accel X : 6
Accel Y : 6
Accel Z : 6
RMS : 6

08
SPV1840LR5H-B
Sound level : 1

09
TSYS01
Temperature : 6

0A
HMC5883L
B Field X : 8
B Field Y : 8
B Field Z : 8

0B
HIH6130
Temperature : 6
Humidity : 6

0C
APDS-9006-020
Light-LUX : 1

0D
TSL260RD
Light : 1

0E
TSL250RD
Light : 1

0F
MLX75305
Light : 1

10
ML8511
UV_index : 1

11
D6T
Temperatures : ?

12
MLX90614
Temperature : 6

13
TMP421
Temperature : 6

14
SPV1840LR5H-B
Sound level : ?

15
Total reducing gases
Concentration : 5

16
Ethanol (C2H5-OH)
Concentration : 5

17
Nitrogen Di-oxide (NO2)
Concentration : 5

18
Ozone (03)
Concentration : 5

19
Hydrogen Sulphide (H2S)
Concentration : 5

1A
Total Oxidizing gases
Concentration : 5

1B
Carbon Monoxide (C0)
Concentration : 5

1C
Sulfur Dioxide (SO2)
Concentration : 5

1D
SHT25
Temperature : 2
Humidity : 2

1E
LPS25H
Temperature : 2
Pressure : 4

1F
Si1145
Light : 1
Light : 1
Light : 1

20
Intel MAC
MAC Address : 3

21
CO ADC Temp
ADC Temperature : 2

22
IAQ/IRR Temp
ADC Temperature : 2

23
O3/NO2 Temp
ADC Temperature : 2

24
SO2/H2S Temp
ADC Temperature : 2

25
CO LMP Temp
ADC Temperature : 2

26
Accelerometer
Accel X : 2
Accel Y : 2
Accel Z : 2
Vib Index : 4

27
Gyro
Orientation X : 2
Orientation Y : 2
Orientation Z : 2
Orientation Index : 4
''')
