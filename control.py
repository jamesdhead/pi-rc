"""Watches the RC car for movement."""
import json
import socket
import sys

def format_command(
    frequency,
    useconds,
    sync_multiplier,
    sync_repeats,
    signal_repeats
):
    """Returns the JSON command string for this command tuple."""
    dead_frequency = 49.890 if frequency < 38 else 26.995
    return json.dumps({
        'synchronization_burst_us': useconds * sync_multiplier,
        'synchronization_spacing_us': useconds,
        'total_synchronizations': sync_repeats,
        'signal_burst_us': useconds,
        'signal_spacing_us': useconds,
        'total_signals': signal_repeats,
        'frequency': frequency,
        'dead_frequency': dead_frequency,
    })


def command_iterator(frequency):
    """Iterates through the frequencies and commands."""
    for useconds in xrange(400, 1200, 100):
        for sync_multiplier in xrange(2, 7):
            for sync_repeats in xrange(2, 7):
                for signal_repeats in xrange(5, 50):
                    yield (
                        frequency,
                        useconds,
                        sync_multiplier,
                        sync_repeats,
                        signal_repeats,
                    )

def input_function(type_cast):
    if sys.version_info.major == 2:
        return lambda message: type_cast(raw_input(message))
    else:
        return lambda message: type_cast(input(message))

def get_command_array():
    read_float = input_function(float)
    read_int = input_function(int)

    frequency = read_float('Frequency? ')
    useconds = read_int('Microseconds? ')
    sync_multiplier = read_int('Synchronization multiplier? ')
    sync_repeats = read_int('Synchronization repeats? ')

    return [
        frequency,
        useconds,
        sync_multiplier,
        sync_repeats,
        0, # Signal repeats, to be read in and configuread later
    ]

def main(host, port):
    """Reads in and runs command sequences."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    command_array = get_command_array()

    read_float = input_function(float)
    read_int = input_function(int)

    while True:
        try:
            command_array[4] = read_int('Signal repeats? ')
        except ValueError:
            pass
        command = format_command(*command_array)
        sock.sendto(command + '\n', (host, 12345))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    else:
        HOST = '192.168.1.3'

    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])
    else:
        PORT = 12345

    main(HOST, PORT)
