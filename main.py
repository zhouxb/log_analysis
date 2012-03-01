import puremvc.patterns.facade
import controller

class AppFacade(puremvc.patterns.facade.Facade):

    STARTUP = "startup"
    INOTIFY = "inotify"
    OTHER = "other"

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
		
		super(AppFacade, self).registerCommand(AppFacade.STARTUP, controller.StartupCommand)
		super(AppFacade, self).registerCommand(AppFacade.INOTIFY, controller.InotifyCommand)
		
		super(AppFacade, self).registerCommand(AppFacade.OTHER, controller.OtherCommand)
		#super(AppFacade, self).registerCommand(AppFacade.WRITE_STARTUP, controller.WriteStartupCommand)
		#super(AppFacade, self).registerCommand(AppFacade.EDIT_STARTUP, controller.EditStartupCommand)
		
		#super(AppFacade, self).registerCommand(AppFacade.ADD_POST, controller.AddPostCommand)
		#super(AppFacade, self).registerCommand(AppFacade.EDIT_POST, controller.EditPostCommand)
		#super(AppFacade, self).registerCommand(AppFacade.DELETE_POST, controller.DeletePostCommand)
		
		
		#super(AppFacade, self).registerCommand(AppFacade.GET_POSTS, controller.GetPostsCommand)

def main():
	facade = AppFacade.getInstance()

if __name__ == "__main__":
	main()

