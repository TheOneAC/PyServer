#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import logging.handlers

from configure import logFileName

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
    def Init(cls,logFileName = logFileName,consoleshow = True):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        rh=logging.handlers.TimedRotatingFileHandler(logFileName,'D')
        fm=logging.Formatter("%(asctime)s  %(levelname)s: %(threadName)s  %(message)s","%Y-%m-%d %H:%M:%S")
        rh.setFormatter(fm)
        logger.addHandler(rh)

        if consoleshow:
            cls.ConsoleShow()

        cls.logTool = logger

    @classmethod
    def warn(cls, msg):
        cls.logTool.warn(msg)    
    @classmethod
    def debug(cls, msg):
        cls.logTool.debug(msg)
    @classmethod
    def error(cls, msg):
        cls.logTool.error(msg)
        
    @classmethod
    def info(cls, msg):
        cls.logTool.info(msg)
        
    @classmethod
    def critical(cls, msg):
        cls.logTool.critical(msg)

if __name__ == "__main__":

    log = LoggerTools()
    log.Init()
    log.error("what")
    log.debug("hello")