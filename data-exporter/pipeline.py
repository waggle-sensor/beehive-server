import binascii
import logging
import re
import struct
from waggle.coresense.utils import decode_frame as decode_frame_v3
from waggle.protocol.v5.decoder import decode_frame as decode_frame_v5
from waggle.protocol.v5.decoder import convert as convert_v5


logger = logging.getLogger('pipeline')
logger.setLevel(logging.INFO)


def trim_python_repr(s):
    if s.startswith("b'"):
        return s[2:-1]
    return s


def trim_coresense_packet(source):
    start = source.index(b'\xaa')
    end = source.rindex(b'\x55')
    return source[start:end + 1]


def reunpack_if_needed(source):
    if source[0] != 0xaa:
        return binascii.unhexlify(source.decode())
    return source


def decode_coresense_3(source):
    source = trim_coresense_packet(source)
    source = reunpack_if_needed(source)
    return decode_frame_v3(source)


drop_raw = [
    'metsense_spv1840lr5h-b',
    'image_histogram_r',
    'image_histogram_g',
    'image_histogram_b',
]

def decode_coresense_4(source):
    source = trim_coresense_packet(source)
    source = reunpack_if_needed(source)

    unpacked_data = decode_frame_v5(source)

    results = {}

    for sensor_id, sensor_data in unpacked_data.items():
        for key, value in sensor_data.items():
            results[key] = {'raw': value}

    for sensor_id, sensor_data in unpacked_data.items():
        try:
            for key, (value, unit) in convert_v5(sensor_data, sensor_id).items():
                if unit == 'raw':
                    results[key] = {'raw': value}
                elif key.startswith('chemsense_at') or key.startswith('chemsense_sh') or key.startswith('chemsense_lp'):
                    results[key] = {'raw': int(value * 100), 'hrf': value, 'hrf_units': unit}
                else:
                    if key not in results:
                        results[key] = {}
                    results[key]['hrf'] = value
                    results[key]['hrf_units'] = unit
        except Exception:
            logger.exception('failed to decode {}'.format(source))

    for key in drop_raw:
        try:
            del results[key]['raw']
        except KeyError:
            continue

    return map_readings_4to3(results)


def decode18(data):
    bincounts = struct.unpack_from('<16H', data, offset=0)
    mtof = [x / 3 for x in struct.unpack_from('<4B', data, offset=32)]
    pmvalues = sorted(struct.unpack_from('<3f', data, offset=50))

    values = {
        'bins': bincounts,
        'mtof': mtof,
        'pm': {'1': pmvalues[0], '2.5': pmvalues[1], '10': pmvalues[2]},
    }

    return values


def decode_alphasense_1(source):
    return decode18(source)


decoders = {
    # 'coresense:3': decode_coresense_3,
    'coresense:4': decode_coresense_4,
    'status:0': decode_coresense_4,
    'image_example:0': decode_coresense_4,
    'spl:0': decode_coresense_4,
}


def decode(row):
    plugin = ':'.join([row.plugin_name, row.plugin_version])

    source = binascii.unhexlify(trim_python_repr(row.data))

    if plugin not in decoders:
        return {}

    return decoders[plugin](source)


template_4to3 = {
    'metsense': {
        'bmp180': {
            'pressure': 'metsense_bmp180_pressure',
            'temperature': 'metsense_bmp180_temperature',
        },
        'hih4030': {
            'humidity': 'metsense_hih4030_humidity',
        },
        'htu21d': {
            'humidity': 'metsense_htu21d_humidity',
            'temperature': 'metsense_htu21d_temperature',
        },
        'mma8452q': {
            'acceleration_x': 'metsense_mma8452q_acc_x',
            'acceleration_y': 'metsense_mma8452q_acc_y',
            'acceleration_z': 'metsense_mma8452q_acc_z',
        },
        'pr103j2': {
            'temperature': 'metsense_pr103j2_temperature',
        },
        'spv1840lr5h_b': {
            'intensity': 'metsense_spv1840lr5h-b',
        },
        'tmp112': {
            'temperature': 'metsense_tmp112',
        },
        'tsl250rd': {
            'intensity': 'metsense_tsl250rd_light',
        },
        'tsys01': {
            'temperature': 'metsense_tsys01_temperature',
        },
        'metsense': {
            'id': 'metsense_id',
        },
    },
    'lightsense': {
        'apds_9006_020': {
            'intensity': 'lightsense_apds_9006_020_light'
        },
        'hih6130': {
            'humidity': 'lightsense_hih6130_humidity',
            'temperature': 'lightsense_hih6130_temperature',
        },
        'hmc5883l': {
            'magnetic_field_x': 'lightsense_hmc5883l_hx',
            'magnetic_field_y': 'lightsense_hmc5883l_hy',
            'magnetic_field_z': 'lightsense_hmc5883l_hz',
        },
        'ml8511': {
            'intensity': 'lightsense_ml8511',
        },
        'mlx75305': {
            'intensity': 'lightsense_mlx75305',
        },
        'tmp421': {
            'temperature': 'lightsense_tmp421',
        },
        'tsl250rd': {
            'intensity': 'lightsense_tsl250_light',
        },
        'tsl260rd': {
            'intensity': 'lightsense_tsl260_light',
        },
    },
    'chemsense': {
        'lps25h': {
            'pressure': 'chemsense_lpp',
            'temperature': 'chemsense_lpt',
        },
        'sht25': {
            'humidity': 'chemsense_shh',
            'temperature': 'chemsense_sht',
        },
        'si1145': {
            'ir_intensity': 'chemsense_sir',
            'uv_intensity': 'chemsense_suv',
            'visible_light_intensity': 'chemsense_svl',
        },
        'chemsense': {
            'id': 'chemsense_id',
        },
        'co': {
            'concentration': 'chemsense_cmo',
        },
        'h2s': {
            'concentration': 'chemsense_h2s',
        },
        'no2': {
            'concentration': 'chemsense_no2',
        },
        'o3': {
            'concentration': 'chemsense_ozo',
        },
        'so2': {
            'concentration': 'chemsense_so2',
        },
        'reducing_gases': {
            'concentration': 'chemsense_irr',
        },
        'oxidizing_gases': {
            'concentration': 'chemsense_iaq',
        },
        'at0': {
            'temperature': 'chemsense_at0',
        },
        'at1': {
            'temperature': 'chemsense_at1',
        },
        'at2': {
            'temperature': 'chemsense_at2',
        },
        'at3': {
            'temperature': 'chemsense_at3',
        },
    },
    'alphasense': {
        'opc_n2': {
            'pm1': 'alphasense_pm1',
            'pm2_5': 'alphasense_pm2.5',
            'pm10': 'alphasense_pm10',
            'bins': 'alphasense_bins',
            'sample_flow_rate': 'alphasense_sample_flow_rate',
            'sampling_period': 'alphasense_sampling_period',
            'id': 'alpha_serial',
            'fw': 'alpha_firmware',
        }
    },
    'plantower': {
        'pms7003': {
            '10um_particle': 'pms7003_10um_particle',
            '1um_particle': 'pms7003_1um_particle',
            '2_5um_particle': 'pms7003_2_5um_particle',
            '5um_particle': 'pms7003_5um_particle',
            'pm10_atm': 'pms7003_pm10_atm',
            'pm10_cf1': 'pms7003_pm10_cf1',
            'pm1_atm': 'pms7003_pm1_atm',
            'pm1_cf1': 'pms7003_pm1_cf1',
            'pm25_atm': 'pms7003_pm25_atm',
            'pm25_cf1': 'pms7003_pm25_cf1',
            'point_3um_particle': 'pms7003_point_3um_particle',
            'point_5um_particle': 'pms7003_point_5um_particle',
        },
    },
    'nc': {
        'uptime': {
            'uptime': 'nc_uptime',
            'idletime': 'nc_idletime',
        },
        'loadavg': {
            'load_1': 'nc_load_1',
            'load_5': 'nc_load_5',
            'load_10': 'nc_load_10',
        },
        'mem': {
            'total': 'nc_ram_total',
            'free': 'nc_ram_free',
        },
        'net_broadband': {
            'rx': 'net_broadband_rx',
            'tx': 'net_broadband_tx',
        },
        'net_lan': {
            'rx': 'net_lan_rx',
            'tx': 'net_lan_tx',
        },
        'net_usb': {
            'rx': 'net_usb_rx',
            'tx': 'net_usb_tx',
        },
    },
    'ep': {
        'uptime': {
            'uptime': 'ep_uptime',
            'idletime': 'ep_idletime',
        },
        'loadavg': {
            'load_1': 'ep_load_1',
            'load_5': 'ep_load_5',
            'load_10': 'ep_load_10',
        },
        'mem': {
            'total': 'ep_ram_total',
            'free': 'ep_ram_free',
        },
    },
    'wagman': {
        'uptime': {
            'uptime': 'wagman_uptime',
        },
        'current': {
            'wagman': 'wagman_current_wagman',
            'nc': 'wagman_current_nc',
            'ep': 'wagman_current_ep',
            'cs': 'wagman_current_cs',
        },
        'failures': {
            'nc': 'wagman_failcount_nc',
            'ep': 'wagman_failcount_ep',
            'cs': 'wagman_failcount_cs',
        },
        'temperatures': {
            'nc_heatsink': 'wagman_temperature_ncheatsink',
            'ep_heatsink': 'wagman_temperature_epheatsink',
            'battery': 'wagman_temperature_battery',
            'brainplate': 'wagman_temperature_brainplate',
            'powersupply': 'wagman_temperature_powersupply',
        },
        'enabled': {
            'nc': 'wagman_enabled_nc',
            'ep': 'wagman_enabled_ep',
            'cs': 'wagman_enabled_cs',
        },
        'heartbeat': {
            'nc': 'wagman_heartbeat_nc',
            'ep': 'wagman_heartbeat_ep',
            'cs': 'wagman_heartbeat_cs',
        },
        'htu21d': {
            'temperature': 'wagman_htu21d_temperature',
            'humidity': 'wagman_htu21d_humidity',
        },
        'hih4030': {
            'humidity': 'wagman_hih4030_humidity',
        },
        'light': {
            'intensity': 'wagman_light',
        },
    },

    #     # 'boot_flags': 'wagman_boot_flag',
    #     # 'nc_bootloader_flags': 'wagman_bootloader_nc_flag',

    # },
    'image': {
        'device': {
            'device': 'image_device',
        },
        'avg': {
            'r': 'image_average_color_r',
            'g': 'image_average_color_g',
            'b': 'image_average_color_b',
        },
        'hist': {
            'r': 'image_histogram_r',
            'g': 'image_histogram_g',
            'b': 'image_histogram_b',
        }
    },
    'audio': {
        'microphone': {
            'octave_1_intensity': 'audio_spl_octave1',
            'octave_2_intensity': 'audio_spl_octave2',
            'octave_3_intensity': 'audio_spl_octave3',
            'octave_4_intensity': 'audio_spl_octave4',
            'octave_5_intensity': 'audio_spl_octave5',
            'octave_6_intensity': 'audio_spl_octave6',
            'octave_7_intensity': 'audio_spl_octave7',
            'octave_8_intensity': 'audio_spl_octave8',
            'octave_9_intensity': 'audio_spl_octave9',
            'octave_10_intensity': 'audio_spl_octave10',
            'octave_total_intensity': 'audio_spl_octave_total',
        }
    }
}


def map_parameters_4to3(readings, parameters):
    output = {}

    for p, k in parameters.items():
        try:
            output[p] = readings[k]
        except KeyError:
            continue

    return output


def map_readings_4to3(readings):
    output = {}

    for subsystem, sensors in template_4to3.items():
        for sensor, parameters in sensors.items():
            output[(subsystem, sensor)] = map_parameters_4to3(readings, parameters)

    return output
