from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
import sys
from .core import EclipseNodeEditor
from .builtin import *


class EclipseNodeEditorApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle("Eclipse Node Editor")

        # Set window size
        window_width = 1400
        window_height = 900

        # Get the screen geometry and calculate center position
        screen = self.app.primaryScreen().geometry()
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2

        # Set the window geometry to be centered
        self.window.setGeometry(x, y, window_width, window_height)

        # Create and set the central widget
        self.editor = EclipseNodeEditor()
        self.window.setCentralWidget(self.editor)

        # Default tools
        self.default_tools = []
        self.add_default_tools()

    def run(self):
        self.window.show()
        return self.app.exec()

    def add_default_tools(self):
        self.default_tools.append(self.editor.add_tool(NodeMovingTool()))
        self.default_tools.append(self.editor.add_tool(NodeConnectionTool()))
        self.default_tools.append(
            self.editor.add_tool(ConnectionRerouteTool()))
        self.default_tools.append(
            self.editor.add_tool(ConnectionCuttingTool()))
        self.default_tools.append(self.editor.add_tool(SelectingTool()))

    def remove_default_tools(self):
        for tool in self.default_tools:
            self.editor.remove_tool(tool)
        self.default_tools = []
