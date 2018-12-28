#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Jude"

import logging

AbyssLogger = logging.getLogger('BuildLogger')
AbyssLogger.setLevel(logging.DEBUG)

def big_log_start(msg):
    AbyssLogger.debug('\n')
    AbyssLogger.debug('********************************************************************************')
    AbyssLogger.debug(msg)
    AbyssLogger.debug('********************************************************************************')


def big_log_end(msg):
    AbyssLogger.debug('********************************************************************************')
    AbyssLogger.debug(msg)
    AbyssLogger.debug('********************************************************************************')
    AbyssLogger.debug('\n')


def debug(msg):
    AbyssLogger.debug("  " + msg)
    return msg


def error(msg):
    AbyssLogger.error("  " + msg)
    return msg
