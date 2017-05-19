#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import logging.handlers



class LoggerTools():
    logTool = None

    @classmethod
    def ConsoleShow(cls):
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    @classmethod
    def Init(cls,logFileName = 'logfile.txt',consoleshow = True):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        rh=logging.handlers.TimedRotatingFileHandler(logFileName,'D')
        fm=logging.Formatter("%(asctime)s  %(levelname)s: %(threadName)s  %(message)s","%Y-%m-%d %H:%M:%S")
        rh.setFormatter(fm)
        logger.addHandler(rh)

        if consoleshow:
            cls.ConsoleShow()

        cls.logTool = logger

    @classmethod
    def warn(cls, msg):
        warn = cls.logTool.warn
        warn(msg)

    @classmethod
    def debug(cls, msg):
        debug = cls.logTool.debug
        debug(msg)
    @classmethod
    def error(cls, msg):
        error = cls.logTool.error
        error(msg)

if __name__ == "__main__":

    log = LoggerTools()
    log.Init()
    log.error("what")
    log.debug("hello")