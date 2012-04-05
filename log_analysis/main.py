#!/usr/bin/python
'''
main module of log_analysis
'''
import puremvc.patterns.facade
import controller
import time

class AppFacade(puremvc.patterns.facade.Facade):
    STARTUP     = "startup"
    PARSEARGS   = "parseargs"
    STARTDAEMON = "startdaemon"
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
            (AppFacade.STARTDAEMON , controller.StartDaemonCommand) ,
            (AppFacade.PARSEARGS   , controller.ParseArgsCommand)   ,
            (AppFacade.MONIT       , controller.MonitCommand)       , 
            (AppFacade.PREPROCESS  , controller.PreprocessCommand)  , 
            (AppFacade.ANALYSIS    , controller.AnalysisCommand)    , 
            (AppFacade.COLLECT     , controller.CollectCommand)     , 
            (AppFacade.POSTPROCESS , controller.PostprocessCommand)
        ]

        for name, cmd in command_table:
            super(AppFacade, self).registerCommand(name, cmd)
def main():
    AppFacade.getInstance()

if __name__ == "__main__":
    main()
    # make sure log process finished everything
    time.sleep(1)
