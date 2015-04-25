#Author - Adam Nagy
#Description - An AddIn that enables the user to keep a snapshot of 
# the current state of the model then compare it to a later state
# of the model

import adsk.core, adsk.fusion, traceback, os
# WebPageDirectory path, where we'll store the images and the html page
wpd = os.path.dirname(os.path.realpath(__file__)) + '/resources/webpage'

# save the current view of the model    
def saveImage(fileName):
    app = adsk.core.Application.get()
    vp = app.activeViewport
    ret = app.activeViewport.saveAsImageFile(fileName, vp.width, vp.height)      
    ui = app.userInterface

    if not ret:
        ui.messageBox('Could not save image')
    
# open the html page that will show the two recorded images    
def showWebPage():
    # show our html file with the content of the two 
    # image files and you can switch between them   
    import webbrowser
    webbrowser.open_new('file://' + wpd + '/comparer.html')    
 
# global set of event handlers to keep them referenced for the duration of the command
handlers = []
saveCommandId = 'ComparerSaveCmd'
viewCommandId = 'ComparerViewCmd'

# some utility functions
def commandDefinitionById(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandDefinition id is not specified')
        return None
    commandDefinitions_ = ui.commandDefinitions
    commandDefinition_ = commandDefinitions_.itemById(id)
    return commandDefinition_

def commandControlByIdForPanel(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandControl id is not specified')
        return None
    workspaces_ = ui.workspaces
    modelingWorkspace_ = workspaces_.itemById('FusionSolidEnvironment')
    toolbarPanels_ = modelingWorkspace_.toolbarPanels
    toolbarPanel_ = toolbarPanels_.item(0)
    toolbarControls_ = toolbarPanel_.controls
    toolbarControl_ = toolbarControls_.itemById(id)
    return toolbarControl_

def destroyObject(uiObj, objToDelete):
    if uiObj and objToDelete:
        if objToDelete.isValid:
            objToDelete.deleteMe()
        else:
            uiObj.messageBox('objToDelete is not a valid object')   

def addCommandToPanel(panel, commandId, commandName, commandDescription, commandResources, onCommandCreated):
    app = adsk.core.Application.get()
    ui = app.userInterface    
    commandDefinitions_ = ui.commandDefinitions
    
    toolbarControlsPanel_ = panel.controls
    toolbarControlPanel_ = toolbarControlsPanel_.itemById(commandId)
    if not toolbarControlPanel_:
        commandDefinitionPanel_ = commandDefinitions_.itemById(commandId)
        if not commandDefinitionPanel_:
            commandDefinitionPanel_ = commandDefinitions_.addButtonDefinition(commandId, commandName, commandDescription, commandResources)
        #onCommandCreated = CommandCreatedEventHandlerPanel()
        commandDefinitionPanel_.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        handlers.append(onCommandCreated)
        toolbarControlPanel_ = toolbarControlsPanel_.addCommand(commandDefinitionPanel_, commandId)
        toolbarControlPanel_.isVisible = True    

def getControlAndDefinition(commandId, objects):
    commandControl_ = commandControlByIdForPanel(commandId)
    if commandControl_:
        objects.append(commandControl_)

    commandDefinition_ = commandDefinitionById(commandId)
    if commandDefinition_:
        objects.append(commandDefinition_)

# the main function that is called when our addin is loaded
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # command properties
        saveCommandName = 'Comparer Save'
        saveCommandDescription = 'Compare Save'
        saveCommandResources = './resources/comparer_save'
        viewCommandName = 'Comparer View'
        viewCommandDescription = 'Compare View'      
        viewCommandResources = './resources/comparer_view'

        # "Comparer Save" command
        class SaveCommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    # delete "current.png" because that should be done
                    # by the "Comparer View" command 
                    try:
                        os.remove(wpd + '/current.png')
                    except:
                        None    
                    
                    # now save image as previous
                    saveImage(wpd + '/previous.png')
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'.format(traceback.format_exc()))

        class SaveCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = SaveCommandExecuteHandler()
                    cmd.execute.add(onExecute)

                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'.format(traceback.format_exc()))
         
        # "Comparer View" command                
        class ViewCommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    # save the current image if it does not exist yet
                    if not os.path.isfile(wpd + '/current.png'):
                        saveImage(wpd + '/current.png')
                    
                    # now open the webpage that shows our two images
                    showWebPage()
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'.format(traceback.format_exc()))

        class ViewCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = ViewCommandExecuteHandler()
                    cmd.execute.add(onExecute)

                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'.format(traceback.format_exc()))                    
        
        # add our commands on create panel in modeling workspace
        workspaces_ = ui.workspaces
        modelingWorkspace_ = workspaces_.itemById('FusionSolidEnvironment')
        toolbarPanels_ = modelingWorkspace_.toolbarPanels
        # add the new commands under the first panel
        toolbarPanel_ = toolbarPanels_.item(0) 
        addCommandToPanel(toolbarPanel_, saveCommandId, saveCommandName, saveCommandDescription, saveCommandResources, SaveCommandCreatedEventHandler())
        addCommandToPanel(toolbarPanel_, viewCommandId, viewCommandName, viewCommandDescription, viewCommandResources, ViewCommandCreatedEventHandler())
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        objArray = []
        
        # Comparer Save
        getControlAndDefinition(saveCommandId, objArray)

        # Comparer View
        getControlAndDefinition(viewCommandId, objArray)
            
        for obj in objArray:
            destroyObject(ui, obj)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
