#!/usr/bin/env python3
# encoding: utf-8

import os
import re
import sys
import math
import logging
import ipaddress

from config import DELEGATED_APNIC_DATA_PATH, CHNROUTE_V4_DATA_PATH, CHNROUTE_V6_DATA_PATH

logging.basicConfig()
logger = logging.getLogger(__name__)

# Only 3 types are includede in the record, so we can only match ipv4/ipv6.
CHNROUTE_V4_REGEX = r"apnic\|cn\|ipv4\|.+"
CHNROUTE_V6_REGEX = r"apnic\|cn\|ipv6\|.+"


def read_delegated_apnic_data(path):
    try:
        with open(path, 'r') as f:
            return f.readlines()
    except Exception as e:
        logger.error(repr(e))
        return []


def parse_chnroute_record(record):
    """
    FORMAT: registry|cc|type|start|value|date|status[ |extensions...]
    """
    _, _, rec_type, rec_start, rec_value = record.split('|')[:5]
    if rec_type == "ipv4":
        # In the case of IPv4 address the count of hosts for this range. This count does not have to represent a CIDR range.
        mask = int(32 - math.log(int(rec_value), 2))
        try:
            network_str = '{}/{}'.format(rec_start, mask)
            net_cidr = ipaddress.IPv4Network(network_str)
            return str(net_cidr)
        except Exception as e:
            logger.error("Failed parse record {}".format(record))
            logger.error(repr(e))
            return ''
    elif rec_type == "ipv6":
        # In the case of an IPv6 address the value will be the CIDR prefix length from the 'first address' value of <start>.
        try:
            network_str = '{}/{}'.format(rec_start, rec_value)
            net_cidr = ipaddress.IPv6Network(network_str)
            return str(net_cidr)
        except Exception as e:
            logger.error("Failed parse record {}".format(record))
            logger.error(repr(e))
            return ''
    return ''


def write_chnroute_data(delegated_apnic_raw_list, chnroute_regex, path):
    r = re.compile(chnroute_regex, re.IGNORECASE)
    chnroute_raw_list = [i for i in delegated_apnic_raw_list if r.match(i)]
    chnroute_list = [parse_chnroute_record(i) for i in chnroute_raw_list]
    chnroute_list_as_bytes = [(i + '\n').encode() for i in chnroute_list]
    try:
        with open(path, 'wb') as f:
            f.writelines(chnroute_list_as_bytes)
        return True
    except Exception as e:
        logger.error(repr(e))
        return False


def main():
    delegated_apnic_raw_list = read_delegated_apnic_data(DELEGATED_APNIC_DATA_PATH)
    if not delegated_apnic_raw_list:
        sys.exit(1)
    ret_v4 = write_chnroute_data(delegated_apnic_raw_list, CHNROUTE_V4_REGEX, CHNROUTE_V4_DATA_PATH)
    ret_v6 = write_chnroute_data(delegated_apnic_raw_list, CHNROUTE_V6_REGEX, CHNROUTE_V6_DATA_PATH)
    if not ret_v4:
        logger.error("WRITE CHNROUTE v4 DATA FAILED...")
    if not ret_v6:
        logger.error("WRITE CHNROUTE V6 DATA FAILED...")
    sys.exit(not (ret_v4 and ret_v6))

if __name__ == '__main__':
    main()