import subprocess
import zlib
from time import sleep
import errno
import os
import string
import random

import iccom_common as iccom_common

# Create an iccom devices and propagate
# the error expectations
#
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def create_iccom_device(err_expectation):
    file = "/sys/class/iccom/create_iccom"
    command = " "
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Delete an iccom devices and propagate
# the error expectations
#
# @iccom_dev {string} iccom device name
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def delete_iccom_device(iccom_dev, err_expectation):
    file = "/sys/class/iccom/delete_iccom"
    command = "%s" % (iccom_dev)
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Create an full duplex test transport device and propagate
# the error expectations
#
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def create_fd_test_transport_device(err_expectation):
    file = "/sys/class/fd_test_transport/create_transport"
    command = " "
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Delete an full duplex test transport device and propagate
# the error expectations
#
# @transport_dev {string} full duplex test device name
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def delete_fd_test_transport_device(transport_dev, err_expectation):
    file = "/sys/class/fd_test_transport/delete_transport"
    command = "%s" % (transport_dev)
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Link an iccom to a full duplex test transport device
# and propagate the error expectations
#
# @transport_dev {string} full duplex test device name
# @iccom_dev {string} iccom device name
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def link_fd_test_transport_device_to_iccom_device(transport_dev, iccom_dev, err_expectation):
    file = "/sys/devices/platform/%s/transport" % (iccom_dev)
    command = transport_dev
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Create an iccom sysfs channel and propagate
# the error expectations
#
# @iccom_dev {string} iccom device name
# @channel {string} sysfs channel number
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def create_iccom_sysfs_channel(iccom_dev, channel, err_expectation):
    file = "/sys/devices/platform/%s/channels_ctl" % (iccom_dev)
    command = "c%d" % (channel)
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Delete an iccom sysfs channel and propagate
# the error expectations
#
# @iccom_dev {string} iccom device name
# @channel {string} sysfs channel number
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def delete_iccom_sysfs_channel(iccom_dev, channel, err_expectation):
    file = "/sys/devices/platform/%s/channels_ctl" % (iccom_dev)
    command = "d%d" % (channel)
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Set the iccom sysfs channel to read or write and propagate
# the error expectations
#
# @iccom_dev {string} iccom device name
# @channel {string} sysfs channel number
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def set_iccom_sysfs_channel(iccom_dev, channel, err_expectation):
    file = "/sys/devices/platform/%s/channels_ctl" % (iccom_dev)
    command = "s%d" % (channel)
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Retrieves the iccom git revision and propagate
# the error expectations
#
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
# Returns:
# Empty String
# String with data read
def iccom_version(err_expectation):
    file = "/sys/class/iccom/version"
    output = iccom_common.read_sysfs_file(file, err_expectation)
    return output

# Writes message to the given iccom sysfs channel
#
# @iccom_dev {string} id of the iccom device
# @channel {number} the destination channel id
# @message {string} message to send
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def iccom_send(iccom_dev, channel, message, err_expectation):
    # Set sysfs channel to work with
    set_iccom_sysfs_channel(iccom_dev, channel, None)
    # Write to the working sysfs channel
    file = "/sys/devices/platform/%s/channels_RW" % (iccom_dev)
    print("iccom_send: " + str(channel))
    command = message
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Reads message from the given iccom sysfs channel and propagate
# the error expectations
#
# @iccom_dev {string} iccom device name
# @channel {string} sysfs channel number
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
# Returns:
# Empty String
# String with data read
def iccom_read(iccom_dev, channel, err_expectation):
    # Set sysfs channel to work with
    set_iccom_sysfs_channel(iccom_dev, channel, None)
    # Read from the working sysfs channel
    file = "/sys/devices/platform/%s/channels_RW" % (iccom_dev)
    print("iccom_read: " + str(channel))
    output = iccom_common.read_sysfs_file(file, err_expectation)
    return output

# Write in the full duplext test transport device the wire
# message that shall be sent later on
#
# @transport_dev {string} full duplex test device name
# @data bytearray to write to wire
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def write_to_wire(transport_dev, data, err_expectation):
    print("iccom_test: simulated wire data: %s" % (data.hex(),))
    file = "/sys/devices/platform/%s/transport_RW" % (transport_dev)
    command = data.hex()
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Reads the data that iccom sent to the wire and propagate
# the error expectations
#
# @transport_dev {string} full duplex test device name
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
#
# RETURNS: the bytarray of wire data sent by ICCom to the wire
def read_from_wire(transport_dev, err_expectation):
    file = "/sys/devices/platform/%s/transport_RW" % (transport_dev)
    output = iccom_common.read_sysfs_file(file, err_expectation)
    result = bytearray.fromhex(output)
    print("iccom_test: received wire data: %s" % (result.hex(),))
    return result

# Performs the full duplex xfer on wire
#
# @transport_dev {string} full duplex test device name
# @send_data the bytearray of the data to send
# @error_R_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
# @error_W_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
#
# RETURNS: the received data as bytearray
def wire_xfer(transport_dev, send_data, error_R_expectation, error_W_expectation):
    write_to_wire(transport_dev, send_data, error_W_expectation)
    sleep(0.1)
    return read_from_wire(transport_dev, error_R_expectation)

# Does the wire full duplex xfer and checks if the
# received data matches expected
#
# @transport_dev {string} full duplex test device name
# @send_data the bytearray of the data to send
# @expected_rcv_data bytearray we expect to receive
# @error_R_expectation {number} the errno which is expected
#                           to be caught on read. Example: None, errno.EIO, ...
# @error_W_expectation {number} the errno which is expected
#                           to be caught on write. Example: None, errno.EIO, ...
# @log_msg the extra message to the log in case of failure
#
# Throws an exception if the received data doesn't match expected
def check_wire_xfer(transport_dev, send_data, expected_rcv_data, error_R_expectation, error_W_expectation, log_msg=""):
    rcv_data = wire_xfer(transport_dev, send_data, error_R_expectation, error_W_expectation)
    if (rcv_data != expected_rcv_data):
        raise RuntimeError("Unexpected data on wire%s!\n"
                           "    %s (expected)\n"
                           "    %s (received)\n"
                           % (" (" + log_msg + ")" if len(log_msg) else ""
                              , expected_rcv_data.hex(), rcv_data.hex()))

# Does the wire full duplex ack xfer and checks if the other side
# acks as well.
#
# @transport_dev {string} full duplex test device name
# @error_R_expectation {number} the errno which is expected
#                           to be caught on read. Example: None, errno.EIO, ...
# @error_W_expectation {number} the errno which is expected
#                           to be caught on write. Example: None, errno.EIO, ...
#  @log_msg the extra message to the log in case of failure
#
# Throws an exception if the other side doesn't ack
def check_wire_xfer_ack(transport_dev, error_R_expectation, error_W_expectation, log_msg=""):
        check_wire_xfer(transport_dev, iccom_ack_package()
                                     , iccom_ack_package()
                        , error_R_expectation, error_W_expectation, log_msg)

# Reads the data from the given channel of given device and checks
# if it matches the expected data.
#
# @iccom_dev {string} iccom device name
# @channel the channel id number
# @expected_ch_data the string which is expected to be received from
#   the channel
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
#
# Throws an exception if the read data doesn't match expected
def check_ch_data(iccom_device, channel, expected_ch_data, expected_error):
    # time is a bad companion, but still we need some time to allow the
    # kernel internals to work all out with 100% guarantee, to allow
    # test stability
    sleep(0.3)
    output = iccom_read(iccom_device, channel, expected_error)

    if(expected_error == None):
        if (output != expected_ch_data):
            raise RuntimeError("Unexpected data mismatch in channel!\n"
                               "    %s (expected)\n"
                               "    %s (received)\n"
                               % (expected_ch_data, output))

# Create the RW sysfs files for a full duplex test device and propagate
# the error expectations
#
# @transport_dev {string} full duplex test device name
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def create_transport_device_RW_files(transport_dev, err_expectation):
    file = "/sys/devices/platform/%s/transport_ctl" % (transport_dev)
    command = "c"
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Deletes the RW sysfs files for a full duplex test device and propagate
# the error expectations
#
# @transport_dev {string} full duplex test device name
# @err_expectation {number} the errno which is expected
#                           to be caught. Example: None, errno.EIO, ...
def delete_transport_device_RW_files(transport_dev, err_expectation):
    file = "/sys/devices/platform/%s/transport_ctl" % (transport_dev)
    command = "d"
    iccom_common.write_sysfs_file(file, command, err_expectation)

# Provides package on the basis of the package payload
# NOTE: by package payload is meant
#   * packets
# NOTE: NOT included
#   * package header
#   * padding
#   * CRC32
#
# @package_sequential_number the sequential number of the package
#   (unsigned byte in size)
# @package_payload the bytearray of the package payload part
#   (packets data)
#
# RETURNS: the new bytearray - a complete package ready to sent
def iccom_package(package_sequential_number, package_payload):
    PACKAGE_SIZE_BYTES = 64
    CRC32_SIZE_BYTES = 4

    if (package_sequential_number > 0xff) or (package_sequential_number < 0):
        raise ValueError("The package_sequential_number must fit the unsigned"
                         " byte in size, but now given: %s"
                         % (str(package_sequential_number)))
    if (len(package_payload) > PACKAGE_SIZE_BYTES - CRC32_SIZE_BYTES):
        raise RuntimeError("The package payload is too big: %d."
                           " It can me max %d bytes size."
                           % (len(package_payload), PACKAGE_SIZE_BYTES - CRC32_SIZE_BYTES))

    package_header = bytearray((len(package_payload)).to_bytes(2, "big")
                               + package_sequential_number.to_bytes(1, "little"))

    padding_size = (PACKAGE_SIZE_BYTES - len(package_header)
                    - len(package_payload) - CRC32_SIZE_BYTES)

    padded_package = package_header + package_payload + bytearray(padding_size * b"\xff")

    crc32 = zlib.crc32(padded_package)

    full_package = padded_package + bytearray(crc32.to_bytes(CRC32_SIZE_BYTES, "little"))

    return full_package

# RETURNS: the bytearray of the ACK iccom package
def iccom_ack_package():
    return bytearray(b"\xd0")

# RETURNS: the bytearray of the NACK iccom package
def iccom_nack_package():
    return bytearray(b"\xe1")

# Renders the ICCom packet raw data.
# @channel an integer, the ICCom channel number (15 bits, unsigned)
# @payload a bytearray with payload to carry
# @complete bool - if set to True, then the packet is marked as the
#   final packet in packet sequence (last packet needed to assemble the
#   final message on the recevier side).
#
# RETURNS: the bytearray for the packet for given @channel
#   with given @payload and completeness flag
def iccom_packet(channel, payload, complete):
    return (len(payload).to_bytes(2, "big")
            + ((channel & 0x7F80) >> 7).to_bytes(1, "big")
            + ((channel & 0x007F) | (0x80 if complete else 0x00)).to_bytes(1, "big")
            + payload )

# Checks the single package for proper on-wire layout generation
# to ensure the tests themselves are testing against proper data.
# @package_seq_id the package sequential ID
# @package_payload the bytearray of the package payload
# @hex_on_wire the raw hex-string which represents the ground-truth
#   of the on-wire data
# @log_msg the message to test
def iccom_tests_sanity_check_package(package_seq_id, package_payload
                , hex_on_wire, log_msg=""):
        expected_data = bytearray.fromhex(hex_on_wire)
        actual_data = iccom_package(package_seq_id, package_payload)
        if (expected_data != actual_data):
                raise RuntimeError("wrong on-wire package image%s!\n"
                                   "    %s (expected)\n"
                                   "    %s (received)\n"
                                   % ((" (" + log_msg + ")" if len(log_msg) else ""
                                       , expected_data.hex(), actual_data.hex())))

# Launches the test given by the callable @test_sequence
# @test_sequence can run in two modes
#   * provides the test info dict
#   * run the actual test sequence and throw in case of any errors
def iccom_test(test_sequence, params):
        try:
            test_info = test_sequence({}, get_test_info=True)
            test_id = test_info["test_id"]
            test_descr = test_info["test_description"]

            print("======== TEST: %s ========" % (test_id,))

            test_sequence(params)

            print("%s: PASS" % (test_id,))
        except Exception as e:
            print("%s: FAILED: %s (test description: %s)" % (test_id, str(e), test_descr))

# Checks if the package testing fits the on-wire picture.
#
# NOTE: this is critically needed to ensure the on-wire compatibility
#   between systems.
def iccom_tests_sanity_check(params, get_test_info=False):

        if (get_test_info):
            return { "test_description":
                        ("checks the on-wire layout for test-generated packages"
                         " to ensure that the tests themselves are on-wire correct")
                     , "test_id": "iccom_test_0.python" }

        ###### Test sequence ######
        iccom_tests_sanity_check_package(217
                , bytearray()
                , "00 00 d9 ff ff ff ff ff ff ff ff ff ff ff ff ff"
                  "ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff"
                  "ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff"
                  "ff ff ff ff ff ff ff ff ff ff ff ff fe 8f 31 00"
                , log_msg="sanity test msg 0")

        iccom_tests_sanity_check_package(219
                , iccom_packet(140, bytearray.fromhex("cd"), True)
                  + iccom_packet(140, bytearray.fromhex("cd"), True)
                  + iccom_packet(140, bytearray.fromhex("cd"), True)
                , "00 0f db 00 01 01 8c cd 00 01 01 8c cd 00 01 01"
                  "8c cd ff ff ff ff ff ff ff ff ff ff ff ff ff ff"
                  "ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff"
                  "ff ff ff ff ff ff ff ff ff ff ff ff 67 2f ba 10"
                , log_msg="sanity test msg 1")

        iccom_tests_sanity_check_package(219
                , iccom_packet(140, bytearray.fromhex("cd"), True)
                  + iccom_packet(140, bytearray.fromhex("cd"), True)
                  + iccom_packet(140, bytearray.fromhex("cd"), True)
                  + iccom_packet(140, bytearray.fromhex("cd"), True)
                , "00 14 db 00 01 01 8c cd 00 01 01 8c cd 00 01 01"
                  "8c cd 00 01 01 8c cd ff ff ff ff ff ff ff ff ff"
                  "ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff"
                  "ff ff ff ff ff ff ff ff ff ff ff ff 25 78 d6 52"
                , log_msg="sanity test msg 2")

        iccom_tests_sanity_check_package(118
                , iccom_packet(139, bytearray.fromhex("cd"), True)
                  + iccom_packet(143, bytearray.fromhex("ff ff"), True)
                  + iccom_packet(139, bytearray.fromhex("cd"), True)
                  + iccom_packet(139, bytearray.fromhex("cd"), True)
                  + iccom_packet(2560, bytearray.fromhex(
                      "ff ff ff ba be 00 14 00 80 0f 31 03 36 2a 09 00"), True)
                  + iccom_packet(139, bytearray.fromhex("cd"), True)
                  + iccom_packet(143, bytearray.fromhex("ff ff"), True)
                  + iccom_packet(139, bytearray.fromhex("cd"), True)
                , "00 39 76 00 01 01 8b cd 00 02 01 8f ff ff 00 01"
                  "01 8b cd 00 01 01 8b cd 00 10 14 80 ff ff ff ba"
                  "be 00 14 00 80 0f 31 03 36 2a 09 00 00 01 01 8b"
                  "cd 00 02 01 8f ff ff 00 01 01 8b cd ae 7d 1e 35"
                , log_msg="sanity test msg 3")

        iccom_tests_sanity_check_package(121
                , iccom_packet(139, bytearray.fromhex("ce"), True)
                  + iccom_packet(139, bytearray.fromhex("ce"), True)
                  + iccom_packet(2560, bytearray.fromhex(
                      "ff ff ff ba be 00 14 00 80 79 85 03 37 2a 09 00"), True)
                  + iccom_packet(143, bytearray.fromhex("ff ff"), True)
                  + iccom_packet(139, bytearray.fromhex("ce"), True)
                  + iccom_packet(139, bytearray.fromhex("ce"), True)
                  + iccom_packet(139, bytearray.fromhex("ce"), True)
                  + iccom_packet(2560, bytearray.fromhex("ff ff"), False)
                , "00 39 79 00 01 01 8b ce 00 01 01 8b ce 00 10 14"
                  "80 ff ff ff ba be 00 14 00 80 79 85 03 37 2a 09"
                  "00 00 02 01 8f ff ff 00 01 01 8b ce 00 01 01 8b"
                  "ce 00 01 01 8b ce 00 02 14 00 ff ff 95 3a 1a b4"
                , log_msg="sanity test msg 4")

        iccom_tests_sanity_check_package(118
                , iccom_packet(139, bytearray.fromhex("cd"), True)
                  + iccom_packet(143, bytearray.fromhex("ff ff"), True)
                  + iccom_packet(139, bytearray.fromhex("cd"), True)
                  + iccom_packet(139, bytearray.fromhex("cd"), False)
                  + iccom_packet(2560, bytearray.fromhex(
                      "ff ff ff ba be 00 14 00 80 0f 31 03 36 2a 09 00"), False)
                  + iccom_packet(139, bytearray.fromhex("cd"), True)
                  + iccom_packet(143, bytearray.fromhex("ff ff"), True)
                  + iccom_packet(139, bytearray.fromhex("cd"), True)
                , "00 39 76 00 01 01 8b cd 00 02 01 8f ff ff 00 01"
                  "01 8b cd 00 01 01 0b cd 00 10 14 00 ff ff ff ba"
                  "be 00 14 00 80 0f 31 03 36 2a 09 00 00 01 01 8b"
                  "cd 00 02 01 8f ff ff 00 01 01 8b cd d4 f7 33 e0"
                , log_msg="sanity test msg 5")

def iccom_data_exchange_to_transport_with_iccom_data_with_transport_data(
                params, get_test_info=False):

        if (get_test_info):
            return { "test_description": ("iccom channel -> wire && wire -> iccom channel")
                     , "test_id": "iccom_test_1.python" }

        transport_dev = params["transport_dev"]
        iccom_dev = params["iccom_dev"]

        ###### Test sequence ######

        create_iccom_sysfs_channel(iccom_dev, 1, None)
        create_transport_device_RW_files(transport_dev, None)

        # Send a message from ICCOM to Full Duplex Test Transport via channel 1
        iccom_send(iccom_dev, 1, "Who are you?", None)

        # Default xfer
        check_wire_xfer(transport_dev, iccom_package(1, bytearray())
                                     , iccom_package(1, bytearray())
                        , None, None, "first data frame")
        check_wire_xfer_ack(transport_dev, None, None, "first ack frame")

        # Actual data xfer
        check_wire_xfer(transport_dev
                        , iccom_package(2, iccom_packet(1, bytearray(b"I am Luis"), True))
                        , iccom_package(2, iccom_packet(1, bytearray(b"Who are you?"), True))
                        , None , None, "second data frame")
        check_wire_xfer_ack(transport_dev, None, None, "second ack frame")

        # Check channel data
        check_ch_data(iccom_dev, 1, "I am Luis", None)

def iccom_data_exchange_to_transport_with_iccom_data_without_transport_data(
                params, get_test_info=False):

        if (get_test_info):
            return { "test_description": ("idle package exchange with"
                                          " expected no data on the channel")
                     , "test_id": "iccom_test_2.python" }

        transport_dev = params["transport_dev"]
        iccom_dev = params["iccom_dev"]

        ###### Test sequence ######

        create_iccom_sysfs_channel(iccom_dev, 1, None)
        create_transport_device_RW_files(transport_dev, None)

        # Do (Default xfer) Data Exchange + ACK
        check_wire_xfer(transport_dev, iccom_package(1, bytearray())
                                     , iccom_package(1, bytearray())
                        , None, None, "first data frame")
        check_wire_xfer_ack(transport_dev, None, None, "first ack frame")

        # Do (Default xfer) Data Exchange + ACK
        check_wire_xfer(transport_dev
                        , iccom_package(2, bytearray())
                        , iccom_package(2, bytearray())
                        , None, None, "second data frame")
        check_wire_xfer_ack(transport_dev, None, None, "second ack frame")

        # Check that there is no channel data
        check_ch_data(iccom_dev, 1, "", errno.EIO)

def iccom_data_exchange_to_transport_with_iccom_data_with_transport_data_wrong_payload_size(
                params, get_test_info=False):

        if (get_test_info):
            return { "test_description": "iccom -> wire && broken wire data package -> iccom"
                     , "test_id": "iccom_test_3.python" }

        transport_dev = params["transport_dev"]
        iccom_dev = params["iccom_dev"]

        ###### Test sequence ######

        create_iccom_sysfs_channel(iccom_dev, 1, None)
        create_transport_device_RW_files(transport_dev, None)

        # Send a message from ICCOM to Full Duplex Test Transport via channel 1
        iccom_send(iccom_dev, 1, "Who are you?", None)

        # Do (Default xfer) Data Exchange + ACK
        check_wire_xfer(transport_dev, iccom_package(1, bytearray())
                                     , iccom_package(1, bytearray())
                        , None, None, "first data frame")
        check_wire_xfer_ack(transport_dev, None, None, "first ack frame")

        # Do (Default xfer) Data Exchange without ACK
        broken_package = iccom_package(2, bytearray())
        broken_package[1] = 0x02;
        check_wire_xfer(transport_dev
                        , broken_package
                        , iccom_package(2, iccom_packet(1, bytearray(b"Who are you?"), True))
                        , None , None, "second data frame")
        check_wire_xfer(transport_dev
                        , iccom_ack_package()
                        , iccom_nack_package()
                        , None , None, "expected nack on wire frame")

        # Check that there is no channel data
        check_ch_data(iccom_dev, 1, "", errno.EIO)

def iccom_data_exchange_to_transport_with_iccom_data_with_transport_nack(
                params, get_test_info=False):

        if (get_test_info):
            return { "test_description": ("iccom -> wire && wire (with nack) -> iccom"
                                          " && repeated transmission iccom -> wire")
                     , "test_id": "iccom_test_4.python" }

        transport_dev = params["transport_dev"]
        iccom_dev = params["iccom_dev"]

        ###### Test sequence ######

        create_iccom_sysfs_channel(iccom_dev, 1000, None)
        create_transport_device_RW_files(transport_dev, None)

        # Send a message from ICCOM to Full Duplex Test Transport via channel 1
        iccom_send(iccom_dev, 1000, "Is there anybody there?", None)

        # Do (Default xfer) Data Exchange + NACK
        check_wire_xfer(transport_dev, iccom_package(1, bytearray())
                                     , iccom_package(1, bytearray())
                        , None, None, "first data frame")
        check_wire_xfer_ack(transport_dev, None, None, "first ack frame")

        # ICCom sends correct data, but we complain that we have not
        # received it properly
        check_wire_xfer(transport_dev
                , iccom_package(2, bytearray())
                , iccom_package(2, iccom_packet(1000, bytearray(b"Is there anybody there?"), True))
                , None, "second data frame")
        check_wire_xfer(transport_dev
                , iccom_nack_package()
                , iccom_ack_package()
                , None, "we send nack")

        # ICCom must repeat the transmission of the data
        check_wire_xfer(transport_dev
                , iccom_package(2, bytearray())
                , iccom_package(2, iccom_packet(1000, bytearray(b"Is there anybody there?"), True))
                , None, "second data frame")
        check_wire_xfer_ack(transport_dev, None, None, "final ack")

        # Check that there is no channel data
        check_ch_data(iccom_dev, 1000, "", errno.EIO)

def iccom_check_devices_deletion(
                params, get_test_info=False):

        if (get_test_info):
            return { "test_description": ("iccom -> check sucessfull removal"
                                          " of all devices")
                     , "test_id": "iccom_test_final_1.python" }

        device_name = params["device_name"]
        number_of_devices = params["number_of_devices"]

        ###### Test sequence ######

        for i in range(number_of_devices):
             iccom_dev = "/sys/devices/platform/%s" % (device_name + str(i))

             # Check that sysfs channel file exists
             iccom_common.check_sysfs_file_presence_expectation(iccom_dev , True)

             delete_iccom_device(device_name + str(i), None)

             # Check that sysfs channel file does not exists
             iccom_common.check_sysfs_file_presence_expectation(iccom_dev , False)

def fd_test_transport_check_devices_deletion(
                params, get_test_info=False):

        if (get_test_info):
            return { "test_description": ("fd_test_transport -> check sucessfull removal"
                                          " of all devices")
                     , "test_id": "iccom_test_final_2.python" }

        device_name = params["device_name"]
        number_of_devices = params["number_of_devices"]

        ###### Test sequence ######

        for i in range(number_of_devices):
             iccom_dev = "/sys/devices/platform/%s" % (device_name + str(i))

             # Check that sysfs channel file exists
             iccom_common.check_sysfs_file_presence_expectation(iccom_dev , True)

             delete_iccom_device(device_name + str(i), None)

             # Check that sysfs channel file does not exists
             iccom_common.check_sysfs_file_presence_expectation(iccom_dev , False)

def iccom_stress_data_communication_with_different_channels(
                params, get_test_info=False):

        if (get_test_info):
            return { "test_description": ("iccom channel -> wire && wire -> iccom channel")
                     , "test_id": "iccom_test_5.python" }

        transport_dev = params["transport_dev"]
        iccom_dev = params["iccom_dev"]

        ###### Test sequence ######
        gen_char_size = 10
        number_of_msgs = 50
        sequence_number = 1
        number_of_channels = 10

        for ch in range(number_of_channels):
            create_iccom_sysfs_channel(iccom_dev, ch, None)

        create_transport_device_RW_files(transport_dev, None)

        for i in range(1, number_of_msgs+1):

            ch = random.randint(0,number_of_channels-1)
            # Increment the size of question and answer
            # which get's generated from 1 to 50 bytes of
            # message
            gen_char_size = i
            print("Test channel: " + str(ch))

            question_str = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=gen_char_size))
            question_b = question_str.encode('utf-8')

            answer_str = ''.join(random.choices(string.ascii_uppercase +
                                    string.digits, k=gen_char_size))
            answer_b = answer_str.encode('utf-8')

            # Send a message from ICCOM to Full Duplex Test Transport via the channel
            iccom_send(iccom_dev, ch, question_str, None)

            # Default Transfer
            check_wire_xfer(transport_dev, iccom_package(sequence_number, bytearray())
                                            , iccom_package(sequence_number, bytearray())
                            , None, None, "default data frame")
            check_wire_xfer_ack(transport_dev, None, None, "ack frame")

            # Data xfer
            check_wire_xfer(transport_dev
                            , iccom_package(sequence_number+1, iccom_packet(ch, bytearray(answer_b), True))
                            , iccom_package(sequence_number+1, iccom_packet(ch, bytearray(question_b), True))
                        , None, None, "data frame")
            check_wire_xfer_ack(transport_dev, None, None, "ack frame")

            # Check channel data
            check_ch_data(iccom_dev, ch, answer_str, None)
            sequence_number += 2


def iccom_data_sysfs_fd_test_transport_RW_creation_deletion_checkup(
                params, get_test_info=False):

        if (get_test_info):
            return { "test_description": ("iccom -> delete R&W files which do not exist")
                     , "test_id": "iccom_test_6.python" }

        transport_dev = params["transport_dev"]
        iccom_dev = params["iccom_dev"]

        ###### Test sequence ######

        transport_RW_file = "/sys/devices/platform/%s/transport_RW" % (transport_dev)

        iccom_common.check_sysfs_file_presence_expectation(transport_RW_file , False)

        create_transport_device_RW_files(transport_dev, None)

        iccom_common.check_sysfs_file_presence_expectation(transport_RW_file , True)

        delete_transport_device_RW_files(transport_dev, None)

        iccom_common.check_sysfs_file_presence_expectation(transport_RW_file , False)

def run_tests(iccom_dev, fd_tt_dev):

        if(len(iccom_dev) != len(fd_tt_dev)):
            print("Aborting! Iccom Tests assume that there will be the same amount of iccom and fd test transport devices")
            return

        number_of_devices = len(iccom_dev)

        output = iccom_version(None)
        print("ICCom revision: " + output)

        try:
           # Link iccom and Full Duplex Test Transport device instances
            for i in range(number_of_devices):
                link_fd_test_transport_device_to_iccom_device(fd_tt_dev[i], iccom_dev[i], None)

        except Exception as e:
            print("[Aborting!] Setup ICCom Tests failed!")
            print(str(e))
            os._exit(os.EX_IOERR)

        # Test #0
        iccom_test(iccom_tests_sanity_check, {})

        # Test #1
        iccom_test(iccom_data_exchange_to_transport_with_iccom_data_with_transport_data
                   , {"transport_dev": fd_tt_dev[0]
                      , "iccom_dev": iccom_dev[0]})

        # Test #2
        iccom_test(iccom_data_exchange_to_transport_with_iccom_data_without_transport_data
                   , {"transport_dev": fd_tt_dev[1]
                      , "iccom_dev": iccom_dev[1]})

        # Test #3
        iccom_test(iccom_data_exchange_to_transport_with_iccom_data_with_transport_data_wrong_payload_size
                   , {"transport_dev": fd_tt_dev[2]
                      , "iccom_dev": iccom_dev[2]})

        #Test #4
        iccom_test(iccom_data_exchange_to_transport_with_iccom_data_with_transport_nack
                   , {"transport_dev": fd_tt_dev[3]
                      , "iccom_dev": iccom_dev[3]})

        #Test #5
        iccom_test(iccom_data_sysfs_fd_test_transport_RW_creation_deletion_checkup
                   , {"transport_dev": fd_tt_dev[4]
                      , "iccom_dev": iccom_dev[4]})

        #Test #6
        iccom_test(iccom_stress_data_communication_with_different_channels
                   , {"transport_dev": fd_tt_dev[5]
                      , "iccom_dev": iccom_dev[5]})

        # Final Test #1
        iccom_test(iccom_check_devices_deletion
                    , {"device_name": "iccom."
                    , "number_of_devices": number_of_devices})

        # Final Test #2
        iccom_test(fd_test_transport_check_devices_deletion
                    , {"device_name": "fd_test_transport."
                    , "number_of_devices": number_of_devices})
