#!/usr/bin/python
'''
main module of log_analysis
'''
import argparse
import puremvc.patterns.facade
import controller

class AppFacade(puremvc.patterns.facade.Facade):
    STARTUP     = "startup"
    MONIT       = "monit"
    PREPROCESS  = "preprocess"
    ANALYSIS    = "analysis"
    COLLECT     = "collect"
    POSTPROCESS = "postprocess"

    def __init__(self):
        self.initializeFacade()
        self.sendNotification(AppFacade.STARTUP)

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeFacade(self):
        super(AppFacade, self).initializeFacade()
        self.initializeController()

    def initializeController(self):
        super(AppFacade, self).initializeController()

        command_table = [
            (AppFacade.STARTUP     , controller.StartupCommand)     , 
            (AppFacade.MONIT       , controller.MonitCommand)       , 
            (AppFacade.PREPROCESS  , controller.PreprocessCommand)  , 
            (AppFacade.ANALYSIS    , controller.AnalysisCommand)    , 
            (AppFacade.COLLECT     , controller.CollectCommand)     , 
            (AppFacade.POSTPROCESS , controller.PostprocessCommand)
        ]

        for name, cmd in command_table:
            super(AppFacade, self).registerCommand(name, cmd)
def main():
    parser = argparse.ArgumentParser("A DNS Log Analysis Program")
    parser.parse_args()
    AppFacade.getInstance()

if __name__ == "__main__":
    main()
