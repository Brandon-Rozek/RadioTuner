#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sat Jun  1 12:54:09 2019
##################################################


from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time
import socket
import re


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.2e6
        self.freq = freq = 101.5e6
        self.audio_rate = audio_rate = 48000
        self.audio_interp = audio_interp = 4

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(0, 0)
        self.rtlsdr_source_0.set_if_gain(0, 0)
        self.rtlsdr_source_0.set_bb_gain(0, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=audio_rate * audio_interp,
                decimation=int(samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'raw_audio_pipe', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=audio_rate * audio_interp,
        	audio_decimation=audio_interp,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate

    def get_audio_interp(self):
        return self.audio_interp

    def set_audio_interp(self, audio_interp):
        self.audio_interp = audio_interp

def is_valid_frequency(frequency):
    return frequency >= 87500000 and frequency <= 108000000

def parse_commands(conn, tb, commands):
    quit = False
    for command in commands:
        if command == "":
            continue
        elif command[0] == '?': # Query Section
            if command[1:] == "VER":
                conn.sendall("Version 0.1\n")
            elif command[1:] == "FREQ":
                conn.sendall(str(tb.get_freq()) + '\n')
            else:
                print("UNKNOWN COMMAND: ", command)
        elif command[0] == ':': # Setter Section
            if command[1:5] == "FREQ":
                print("FREQUENCY SET")
                frequency = float(command[6:])
                if is_valid_frequency(frequency):
                    tb.set_freq(frequency)
                else:
                    print("ERROR: Invalid Frequency ", frequency)
            elif command[1:] == "QUIT":
                print("QUITTING")
                quit = True
            else:
                print("UNKNOWN COMMAND: ", command)
        else:
            print("UNKNOWN COMMAND", command)
    # Return state back to application
    return {'quit': quit}


def main(top_block_cls=top_block, options=None):
    tb = top_block_cls()
    tb.start()

    HOST = '127.0.0.1' # Loopback Address (Localhost)
    PORT = 65432 # Semi-Random Port that is non-priviledged (> 1023)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    quit = False
    while not quit:
        s.listen(1) # Number of unaccepted connections before it rejects new ones
        conn, addr = s.accept()
        print("Connected by ", addr)
        while not quit:
            data = conn.recv(1024) # Not sure about the bytes argument...
            data = data.strip() # Removes \r\n
            print("DATA: ", data)
            commands = re.split(";", data)
            if data == "":
                break
            state = parse_commands(conn, tb, commands)
            if state['quit']:
                quit = True
        conn.close()
    s.close()


if __name__ == '__main__':
    main()
