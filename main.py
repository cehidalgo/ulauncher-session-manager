from asyncio import subprocess
from dataclasses import dataclass
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import subprocess


class Terminal_Runner(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ExecuteSession())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):


        options = []


        for i in range(6):

            data = { "option": i }

            iconStyle = extension.preferences["icon"]

            if iconStyle == "color": optionIcon = "images/icon.png"
            if iconStyle == "black": optionIcon = "images/icon-black.png"
            if iconStyle == "white": optionIcon = "images/icon-white.png"

            if i == 0: optionName = "Shutdown"

            if i == 1: optionName = "Reboot"

            if i == 2: optionName = "Lock"

            if i == 3: optionName = "Suspend"

            if i == 4: optionName = "Logout"

            if i == 5: optionName = "Hibernate"


            options.append(ExtensionResultItem(icon=optionIcon,
                                                    name=optionName,
                                                    on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        return RenderResultListAction(options)


class ExecuteSession(EventListener):

    def on_event(self, event, extension):

        data = event.get_data()
        
        option = data["option"]


        if option == 0: command = "gnome-session-quit --power-off"
        if option == 1: command = "gnome-session-quit --reboot"
        if option == 2: command = "xdg-screensaver lock"
        if option == 3: command = "systemctl suspend"
        if option == 4:

            desktopEnvironment = extension.preferences["desktop-environment"]

            if(desktopEnvironment == "gnome"): command = "gnome-session-quit"
            if(desktopEnvironment == "kde"): command = "qdbus org.kde.ksmserver /KSMServer logout 0 0 1"

        if option == 5: command = "systemctl hibernate"
        
        subprocess.run( [command], shell=True )

        return HideWindowAction()



if __name__ == '__main__':
    Terminal_Runner().run()