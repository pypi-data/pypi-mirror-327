from __future__ import annotations
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QSize, QPoint, QTimer
from PyQt6.QtGui import QColor, QFont, QPainter
from OpenGL.GL import *
import math
from PyQt6.QtWidgets import QApplication
from typing import Callable, Optional
from PyQt6.QtGui import QColor
import math
from .utils import line_intersection
from .input_binding import InputBindingSystem

_socket_registry = {}
_node_registry = {}
_tool_registry = {}


class NodeEditorObject():
    def __init__(self):
        self.raycast_hit = False

    def raycast_reset(self, editor: EclipseNodeEditor):
        """Reset the raycast hit"""
        pass

    def raycast(self, editor: EclipseNodeEditor):
        """Handle input for this object"""
        return False

    def input(self, editor: EclipseNodeEditor):
        """Handle input for this object"""
        pass

    def update(self, editor: EclipseNodeEditor):
        """Update object state"""
        pass

    def render(self, editor: EclipseNodeEditor):
        """Render the object"""
        pass


class Tool():
    def __init__(self):
        self.is_active = True
        self.has_setup = False

    def setup(self, editor: EclipseNodeEditor):
        pass

    def input(self, editor: EclipseNodeEditor):
        pass

    def update(self, editor: EclipseNodeEditor):
        pass

    def render(self, editor: EclipseNodeEditor):
        pass


class EclipseNodeEditor(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configure OpenGL format for antialiasing
        format = self.format()
        format.setSamples(4)  # Use 4x multisampling
        self.setFormat(format)

        self.background_color = QColor(21, 21, 21)
        # Set update behavior to redraw continuously
        self.setUpdateBehavior(QOpenGLWidget.UpdateBehavior.NoPartialUpdate)

        # Enable mouse tracking for smooth pan updates
        self.setMouseTracking(True)

        # Enable key tracking
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Initialize view transform (current values)
        self.pan_x = 0
        self.pan_y = 0
        self.zoom = 1.0

        # Target transform values
        self.target_pan_x = 0
        self.target_pan_y = 0
        self.target_zoom = 1.0

        # Transform constraints
        self.min_zoom = 0.1
        self.max_zoom = 10.0

        # Interpolation settings
        self.lerp_factor = 0.2

        # Mouse state
        self.screen_mouse_pos = QPoint()
        self.world_mouse_pos = QPoint()
        self.last_mouse_drag_pos = QPoint()
        self.is_panning = False
        self.left_mouse_down_prev = False
        self.left_mouse_down = False
        self.left_mouse_pressed = False
        self.left_mouse_released = False
        self.right_mouse_down_prev = False
        self.right_mouse_down = False
        self.right_mouse_pressed = False
        self.right_mouse_released = False

        # Keyboard state
        self.keys_down = set()
        self.keys_pressed = set()
        self.keys_released = set()
        self.modifiers_down = set()
        self.modifiers_pressed = set()
        self.modifiers_released = set()

        # Render groups
        self.render_groups = {}

        # Objects list
        self.objects = []
        self.grabbed_object = None

        # Tools list
        self.tools = []
        self.locked_tool = None
        self.tool_unlocking = False
        # QPainter for text rendering
        self.painter = QPainter()

        # Setup update timer for smooth interpolation and object updates
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.on_timer_update)
        self.update_timer.start(16)  # ~60 FPS

        # Input binding system
        self.input_bindings = InputBindingSystem()

    def add_object(self, obj):
        """Add an object to the editor"""
        self.objects.append(obj)
        return obj

    def remove_object(self, obj):
        """Remove an object from the editor"""
        if obj in self.objects:
            self.objects.remove(obj)

    def get_objects_of_type(self, *args):
        """Get all objects of a given type"""
        objects = []
        for obj in self.objects:
            for arg in args:
                if isinstance(obj, arg):
                    objects.append(obj)
        return objects

    def add_tool(self, tool: Tool):
        """Add a tool to the editor"""
        self.tools.append(tool)
        if not tool.has_setup:
            tool.setup(self)
            tool.has_setup = True
        return tool

    def remove_tool(self, tool: Tool):
        """Remove a tool from the editor"""
        if tool in self.tools:
            self.tools.remove(tool)

    def lock_tool(self, tool: Tool):
        """Lock a tool to the editor"""
        self.locked_tool = tool

    def unlock_tool(self):
        """Unlock a tool from the editor"""
        self.tool_unlocking = True
        self.locked_tool = None

    def on_timer_update(self):
        """Handle timer updates for transform interpolation and object updates"""

        # Update current mouse position
        self.screen_mouse_pos = self.mapFromGlobal(self.cursor().pos())

        # Update world mouse position
        world_x, world_y = self.screen_to_world(
            self.screen_mouse_pos.x(), self.screen_mouse_pos.y())
        self.world_mouse_pos.setX(int(world_x))
        self.world_mouse_pos.setY(int(world_y))

        # Update mouse button states
        self.left_mouse_down_prev = self.left_mouse_down
        self.right_mouse_down_prev = self.right_mouse_down
        buttons = QApplication.mouseButtons()
        self.left_mouse_down = bool(buttons & Qt.MouseButton.LeftButton)
        self.right_mouse_down = bool(buttons & Qt.MouseButton.RightButton)
        self.left_mouse_pressed = self.left_mouse_down and not self.left_mouse_down_prev
        self.left_mouse_released = not self.left_mouse_down and self.left_mouse_down_prev
        self.right_mouse_pressed = self.right_mouse_down and not self.right_mouse_down_prev
        self.right_mouse_released = not self.right_mouse_down and self.right_mouse_down_prev

        # Update modifier states
        current_modifiers = QApplication.keyboardModifiers()

        # Track pressed and released states for modifiers
        for modifier in [Qt.KeyboardModifier.ShiftModifier, Qt.KeyboardModifier.ControlModifier, Qt.KeyboardModifier.AltModifier]:
            is_down = bool(current_modifiers & modifier)
            was_down = modifier in self.modifiers_down

            if is_down and not was_down:
                self.modifiers_pressed.add(modifier)
                self.modifiers_down.add(modifier)
            elif not is_down and was_down:
                self.modifiers_released.add(modifier)
                self.modifiers_down.remove(modifier)

        # First handle transform interpolation
        self.interpolate_transform()

        # Then update all objects
        self.process_objects()

        # Clear one-frame states at the END of the frame, after all processing is done
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.modifiers_pressed.clear()
        self.modifiers_released.clear()

    def process_objects(self):
        """Process input and updates for all objects"""
        self.tool_unlocking = False

        # Reset raycast hit
        for obj in self.objects:
            # Raycast hit is more core to the object so we handle that manually
            obj.raycast_hit = False
            obj.raycast_reset(self)

        # Raycast all objects
        for obj in reversed(self.objects):
            if obj.raycast(self):
                obj.raycast_hit = True
                if self.grabbed_object == None and self.left_mouse_down:
                    self.grabbed_object = obj
                break

        if self.left_mouse_released:
            self.grabbed_object = None

        # Process all inputs
        for obj in self.objects:
            obj.input(self)

        # Process all tools
        for tool in self.tools:
            if tool.is_active:
                if self.locked_tool == None:
                    if not self.tool_unlocking:
                        tool.input(self)
                elif self.locked_tool == tool:
                    tool.input(self)

        # Update all objects
        for obj in self.objects:
            obj.update(self)

        # Update all tools
        for tool in self.tools:
            if tool.is_active:
                if self.locked_tool == None:
                    if not self.tool_unlocking:
                        tool.update(self)
                elif self.locked_tool == tool:
                    tool.update(self)

    def get_mouse_pos(self):
        return self.world_mouse_pos.x(), self.world_mouse_pos.y()

    def add_render_group(self, group_index: int, callback: Callable):
        """Adds a callback to a list for this group index"""
        if group_index not in self.render_groups:
            self.render_groups[group_index] = []
        self.render_groups[group_index].append(callback)

    def render_objects(self):
        """Render all objects"""
        # Clear stored render groups
        self.render_groups = {}

        # Call all render methods
        for obj in self.objects:
            obj.render(self)

        # Call all tool render methods
        for tool in self.tools:
            if tool.is_active:
                if self.locked_tool == None:
                    if not self.tool_unlocking:
                        tool.render(self)
                elif self.locked_tool == tool:
                    tool.render(self)

        # Sort render groups and call callbacks in order
        sorted_groups = sorted(self.render_groups.keys())
        for group_index in sorted_groups:
            for callback in self.render_groups[group_index]:
                callback()

    def lerp(self, start, end, factor):
        """Linear interpolation between start and end values"""
        return start + (end - start) * factor

    def interpolate_transform(self):
        """Interpolate between current and target transform values"""
        # Check if we need to update pan
        if abs(self.target_pan_x - self.pan_x) > 0.01 or abs(self.target_pan_y - self.pan_y) > 0.01:
            self.pan_x = self.lerp(
                self.pan_x, self.target_pan_x, self.lerp_factor)
            self.pan_y = self.lerp(
                self.pan_y, self.target_pan_y, self.lerp_factor)

        # Check if we need to update zoom
        if abs(self.target_zoom - self.zoom) > 0.0001:
            self.zoom = self.lerp(
                self.zoom, self.target_zoom, self.lerp_factor)

        # Always update to ensure continuous frame updates
        self.update()

    def initializeGL(self):
        """Initialize OpenGL settings"""
        glClearColor(21/255, 21/255, 21/255, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Enable multisampling for antialiasing
        glEnable(GL_MULTISAMPLE)
        # Enable line smoothing for better line antialiasing
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    def draw_rectangle(self, x, y, width, height, r, g, b, a=1.0):
        """Helper method to draw a rectangle"""
        glColor4f(r, g, b, a)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    def draw_rectangle_outline(self, x, y, width, height, r, g, b, a=1.0, thickness=1.0):
        """Helper method to draw a rectangle outline with specified thickness"""
        glColor4f(r, g, b, a)

        # Draw top line
        glBegin(GL_QUADS)
        glVertex2f(x - thickness/2, y - thickness/2)
        glVertex2f(x + width + thickness/2, y - thickness/2)
        glVertex2f(x + width + thickness/2, y + thickness/2)
        glVertex2f(x - thickness/2, y + thickness/2)
        glEnd()

        # Draw bottom line
        glBegin(GL_QUADS)
        glVertex2f(x - thickness/2, y + height - thickness/2)
        glVertex2f(x + width + thickness/2, y + height - thickness/2)
        glVertex2f(x + width + thickness/2, y + height + thickness/2)
        glVertex2f(x - thickness/2, y + height + thickness/2)
        glEnd()

        # Draw left line
        glBegin(GL_QUADS)
        glVertex2f(x - thickness/2, y + thickness/2)
        glVertex2f(x + thickness/2, y + thickness/2)
        glVertex2f(x + thickness/2, y + height - thickness/2)
        glVertex2f(x - thickness/2, y + height - thickness/2)
        glEnd()

        # Draw right line
        glBegin(GL_QUADS)
        glVertex2f(x + width - thickness/2, y + thickness/2)
        glVertex2f(x + width + thickness/2, y + thickness/2)
        glVertex2f(x + width + thickness/2, y + height - thickness/2)
        glVertex2f(x + width - thickness/2, y + height - thickness/2)
        glEnd()

    def draw_text(self, x, y, text, r, g, b, a=1.0, font_size=12):
        """Helper method to draw text using Qt's painter"""
        # Start QPainter
        self.painter.begin(self)
        self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set up the font
        font = QFont()
        font.setPointSizeF(font_size * self.zoom)
        self.painter.setFont(font)

        # Set color
        self.painter.setPen(
            QColor(int(r * 255), int(g * 255), int(b * 255), int(a * 255)))

        # Convert position to screen space
        screen_x = x * self.zoom + self.pan_x
        screen_y = y * self.zoom + self.pan_y

        # Get font metrics for proper vertical centering
        metrics = self.painter.fontMetrics()
        text_height = metrics.height()

        # Draw the text centered vertically (y is the center point)
        # Subtract half the text height to center it vertically
        self.painter.drawText(int(screen_x), int(
            screen_y - text_height/2 + metrics.ascent()), text)

        # End QPainter
        self.painter.end()

        # Restore OpenGL state
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.apply_transform()

    def draw_circle(self, x, y, radius, r, g, b, a=1.0):
        """Helper method to draw a circle"""
        glColor4f(r, g, b, a)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)  # Center point
        segments = 32  # Number of segments to make the circle smooth
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            dx = radius * math.cos(angle)
            dy = radius * math.sin(angle)
            glVertex2f(x + dx, y + dy)
        glEnd()

    def draw_circle_outline(self, x, y, radius, r, g, b, a=1.0, thickness=1.0, segments=32):
        """Helper method to draw a circle outline with specified thickness"""
        glColor4f(r, g, b, a)

        # Draw the outline using triangle strip
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            # Calculate outer and inner points
            outer_x = x + (radius + thickness/2) * math.cos(angle)
            outer_y = y + (radius + thickness/2) * math.sin(angle)
            inner_x = x + (radius - thickness/2) * math.cos(angle)
            inner_y = y + (radius - thickness/2) * math.sin(angle)
            # Add both points to create the strip
            glVertex2f(outer_x, outer_y)
            glVertex2f(inner_x, inner_y)
        glEnd()

    def draw_line(self, ax, ay, bx, by, thickness,
                  start_r, start_g, start_b, start_a=1.0,
                  end_r=None, end_g=None, end_b=None, end_a=None):
        """Draw a line with gradient between two colors"""
        # Set end color to start color if not specified
        end_r = start_r if end_r is None else end_r
        end_g = start_g if end_g is None else end_g
        end_b = start_b if end_b is None else end_b
        end_a = start_a if end_a is None else end_a

        # Calculate the direction vector of the line
        dx = bx - ax
        dy = by - ay
        length = math.sqrt(dx * dx + dy * dy)

        if length < 0.0001:  # Avoid division by zero for very short lines
            return

        # Calculate the normalized perpendicular vector
        nx = -dy / length * thickness / 2
        ny = dx / length * thickness / 2

        # Draw the quad with color interpolation
        glBegin(GL_QUADS)
        # Start color for first two vertices
        glColor4f(start_r, start_g, start_b, start_a)
        glVertex2f(ax + nx, ay + ny)
        glVertex2f(ax - nx, ay - ny)
        # End color for last two vertices
        glColor4f(end_r, end_g, end_b, end_a)
        glVertex2f(bx - nx, by - ny)
        glVertex2f(bx + nx, by + ny)
        glEnd()

    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        world_x = (screen_x - self.pan_x) / self.zoom
        world_y = (screen_y - self.pan_y) / self.zoom
        return world_x, world_y

    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x * self.zoom + self.pan_x
        screen_y = world_y * self.zoom + self.pan_y
        return screen_x, screen_y

    def apply_transform(self):
        """Apply the current view transform"""
        width = self.width()
        height = self.height()

        # Set up orthographic projection
        glLoadIdentity()
        glOrtho(0, width, height, 0, -1, 1)

        # Apply transforms in correct order
        glTranslatef(self.pan_x, self.pan_y, 0)
        glScalef(self.zoom, self.zoom, 1.0)

    def paintGL(self):
        """Paint the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Apply the view transform
        self.apply_transform()

        # Render all objects
        self.render_objects()

    def resizeGL(self, width, height):
        """Handle window resize"""
        glViewport(0, 0, width, height)

    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = True
            self.last_mouse_drag_pos = event.pos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events"""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = False
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move events"""
        # Update current mouse position
        if self.is_panning:
            delta = event.pos() - self.last_mouse_drag_pos
            self.target_pan_x += delta.x()
            self.target_pan_y += delta.y()
            self.last_mouse_drag_pos = event.pos()
        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming"""
        # Get mouse position
        mouse_pos = event.position()
        mouse_x = mouse_pos.x()
        mouse_y = mouse_pos.y()

        # Get the world point under mouse before zoom
        old_world_x, old_world_y = self.screen_to_world(mouse_x, mouse_y)

        # Calculate and clamp new zoom level
        zoom_factor = 1.2 if event.angleDelta().y() > 0 else 1/1.2
        new_zoom = self.target_zoom * zoom_factor

        if self.min_zoom <= new_zoom <= self.max_zoom:
            # Set target zoom
            self.target_zoom = new_zoom

            # Calculate the screen point for this world position at target zoom
            # We need to use current pan but target zoom for this calculation
            screen_x = old_world_x * new_zoom + self.target_pan_x
            screen_y = old_world_y * new_zoom + self.target_pan_y

            # Set target pan to keep world point under mouse
            self.target_pan_x += mouse_x - screen_x
            self.target_pan_y += mouse_y - screen_y

        event.accept()

    def keyPressEvent(self, event):
        """Handle key press events"""
        key = event.key()

        # Only handle regular keys here, modifiers are handled in timer update
        if key not in self.keys_down and key not in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            self.keys_pressed.add(key)
            self.keys_down.add(key)

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Handle key release events"""
        key = event.key()

        # Only handle regular keys here, modifiers are handled in timer update
        if key in self.keys_down:
            self.keys_released.add(key)
            self.keys_down.remove(key)

        super().keyReleaseEvent(event)

    def get_key(self, key: int) -> bool:
        """Check if a key is currently held down"""
        if key in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            modifier_map = {
                Qt.Key.Key_Shift: Qt.KeyboardModifier.ShiftModifier,
                Qt.Key.Key_Control: Qt.KeyboardModifier.ControlModifier,
                Qt.Key.Key_Alt: Qt.KeyboardModifier.AltModifier,
                Qt.Key.Key_Meta: Qt.KeyboardModifier.MetaModifier
            }
            return modifier_map[key] in self.modifiers_down
        return key in self.keys_down

    def get_key_down(self, key: int) -> bool:
        """Check if a key was just pressed this frame"""
        if key in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            modifier_map = {
                Qt.Key.Key_Shift: Qt.KeyboardModifier.ShiftModifier,
                Qt.Key.Key_Control: Qt.KeyboardModifier.ControlModifier,
                Qt.Key.Key_Alt: Qt.KeyboardModifier.AltModifier,
                Qt.Key.Key_Meta: Qt.KeyboardModifier.MetaModifier
            }
            return modifier_map[key] in self.modifiers_pressed
        return key in self.keys_pressed

    def get_key_up(self, key: int) -> bool:
        """Check if a key was just released this frame"""
        if key in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            modifier_map = {
                Qt.Key.Key_Shift: Qt.KeyboardModifier.ShiftModifier,
                Qt.Key.Key_Control: Qt.KeyboardModifier.ControlModifier,
                Qt.Key.Key_Alt: Qt.KeyboardModifier.AltModifier,
                Qt.Key.Key_Meta: Qt.KeyboardModifier.MetaModifier
            }
            return modifier_map[key] in self.modifiers_released
        return key in self.keys_released

    def minimumSizeHint(self):
        """Ensure the widget has a minimum size"""
        return QSize(50, 50)

    def sizeHint(self):
        """Preferred size for the widget"""
        return QSize(400, 400)

    def focusInEvent(self, event):
        """Handle focus gained"""
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """Handle focus lost"""
        super().focusOutEvent(event)

    def get_binding(self, name: str) -> bool:
        """Check if a specific input binding is active"""
        return self.input_bindings.check_binding(name)

    def register_binding(self, name: str, priority: int, callback: Callable[[], bool], description: str = ""):
        """Register a new input binding"""
        self.input_bindings.register_binding(
            name, priority, callback, description)

    def remove_binding(self, name: str):
        """Remove an input binding"""
        self.input_bindings.remove_binding(name)

    def get_active_binding(self) -> Optional[str]:
        """Get the currently active binding"""
        return self.input_bindings.get_active_binding()

    def clear_active_binding(self):
        """Clear the currently active binding"""
        self.input_bindings.clear_active_binding()


def socket(*, key=None):
    """Decorator to register Socket subclasses in the socket registry"""
    def decorator(cls):
        registry_key = key or cls.__name__
        _socket_registry[registry_key] = cls
        return cls
    return decorator


def node(*, key=None):
    """Decorator to register Node subclasses in the node registry"""
    def decorator(cls):
        registry_key = key or cls.__name__
        _node_registry[registry_key] = cls
        return cls
    return decorator


def tool(*, key=None):
    """Decorator to register NodeEditorTool subclasses in the tool registry"""
    def decorator(cls):
        registry_key = key or cls.__name__
        _tool_registry[registry_key] = cls
        return cls


class Reroute:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.radius = 5
        self.hover_radius = 7
        self.color = QColor(255, 255, 255)
        self.is_selected = False
        self.is_hovered = False
        self.start_x = x
        self.start_y = y

    def render(self, editor: EclipseNodeEditor):
        editor.draw_circle(
            self.x, self.y, self.hover_radius if self.is_hovered else self.radius, self.color.red() / 255, self.color.green() / 255, self.color.blue() / 255, 1)
        if self.is_selected:
            editor.draw_circle_outline(
                self.x, self.y, self.radius + 10, self.color.red() / 255, self.color.green() / 255, self.color.blue() / 255, 1, 2)


class SocketConnection:
    def __init__(self):
        self.from_node: Node | None = None
        self.from_socket: Socket | None = None
        self.to_node: Node | None = None
        self.to_socket: Socket | None = None
        self.reroutes: list[Reroute] = []


class Socket(NodeEditorObject):
    def __init__(self):
        super().__init__()
        self.connected_height = 25
        self.width = 0
        self.height = 25
        self.pin_radius = 5
        self.pin_hover_radius = 7
        self.pin_color = QColor(255, 255, 255)
        self.pin_type = "input"
        self.connections: list[SocketConnection] = []
        self.is_hovered = False
        self.is_pin_hovered = False

    def render_pin(self, node: Node, x: int, y: int, editor: EclipseNodeEditor):
        pin_x = x
        if self.pin_type == "input":
            pin_x = x

        if self.pin_type == "output":
            pin_x = x + node.width

        editor.draw_circle(pin_x, y + self.connected_height / 2, self.pin_hover_radius if self.is_pin_hovered else self.pin_radius,
                           self.pin_color.red() / 255,
                           self.pin_color.green() / 255,
                           self.pin_color.blue() / 255)

    def check_show_interface(self):
        if self.pin_type == "output":
            return False

        if self.pin_type == "input":
            if self.connections:
                return False

        return True


class Node(NodeEditorObject):
    def __init__(self, x=0, y=0, title="Node"):

        super().__init__()
        # Position and size
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100

        # Colors
        self.primary_color = QColor(75, 75, 75)    # Header color
        self.secondary_color = QColor(50, 50, 50)  # Background color
        self.title_color = QColor(255, 255, 255)   # Title text color

        # Title properties
        self.title = title
        self.title_font_size = 12
        self.header_size = 30

        # State
        self.is_selected = False
        self.is_hovered = False
        self.is_over_header = False
        self.start_mouse_x = 0
        self.start_mouse_y = 0
        self.start_x = 0
        self.start_y = 0
        self.is_selected = False

        # Sockets
        self.sockets: list[Socket] = []
        self.sockets_spacing = 2
        self.render_socket_regions = False

    def add_input_socket(self, socket: Socket):
        socket.pin_type = "input"
        self.sockets.append(socket)
        return socket

    def add_output_socket(self, socket: Socket):
        socket.pin_type = "output"
        self.sockets.append(socket)
        return socket

    def raycast_reset(self, editor: EclipseNodeEditor):
        self.is_hovered = False
        self.is_over_header = False
        for socket in self.sockets:
            socket.is_hovered = False
            socket.is_pin_hovered = False
            for connection in socket.connections:
                connection: SocketConnection
                for reroute in connection.reroutes:
                    reroute.is_hovered = False

    def raycast(self, editor: EclipseNodeEditor):
        mouse_x, mouse_y = editor.get_mouse_pos()
        has_hit = False

        # Check if the mouse is over the node
        if mouse_x >= self.x and mouse_x <= self.x + self.width and mouse_y >= self.y and mouse_y <= self.y + self.height:
            has_hit = True
            self.is_hovered = True

            if mouse_y <= self.y + self.header_size:
                self.is_over_header = True

        # Check if the mouse is over the sockets
        socket_y = self.y + self.header_size
        for i, socket in enumerate(self.sockets):
            if mouse_x >= self.x and mouse_x <= self.x + self.width and mouse_y >= socket_y and mouse_y <= socket_y + (socket.connected_height if socket.connections else socket.height):
                socket.is_hovered = True
                has_hit = True

            dist = math.sqrt((mouse_x - self.get_socket_x(socket))
                             ** 2 + (mouse_y - (socket_y + socket.connected_height / 2)) ** 2)
            if dist <= socket.pin_hover_radius:
                socket.is_pin_hovered = True
                has_hit = True

            for connection in socket.connections:
                connection: SocketConnection
                for reroute in connection.reroutes:
                    reroute_dist = math.sqrt(
                        (mouse_x - reroute.x) ** 2 + (mouse_y - reroute.y) ** 2)
                    if reroute_dist <= reroute.hover_radius:
                        reroute.is_hovered = True

            show_interface = socket.check_show_interface()
            if show_interface:
                socket_y += socket.height + self.sockets_spacing
            else:
                socket_y += socket.connected_height + self.sockets_spacing

        return has_hit

    def update(self, editor: EclipseNodeEditor):
        """Update node state"""
        width_needed = self.width
        height_needed = self.header_size
        for socket in self.sockets:
            width_needed = max(width_needed, socket.width)
            show_interface = socket.check_show_interface()
            if show_interface:
                height_needed += socket.height + self.sockets_spacing
            else:
                height_needed += socket.connected_height + self.sockets_spacing

        self.width = width_needed
        self.height = height_needed

    def render(self, editor: EclipseNodeEditor):
        """Render the node"""
        def render_pass_node():
            # Draw outer shadow first (larger and more transparent)
            outer_shadow_offset = 6
            outer_shadow_expand = 4
            editor.draw_rectangle(
                self.x - outer_shadow_expand,
                self.y + outer_shadow_offset - outer_shadow_expand - 6,
                self.width + outer_shadow_expand * 2,
                self.height + outer_shadow_expand * 4,
                0, 0, 0, 0.15  # Very transparent black
            )

            # Draw inner shadow (smaller and more opaque)
            inner_shadow_offset = 4
            inner_shadow_expand = 2
            editor.draw_rectangle(
                self.x - inner_shadow_expand,
                self.y + inner_shadow_offset - inner_shadow_expand - 4,
                self.width + inner_shadow_expand * 2,
                self.height + inner_shadow_expand * 4,
                0, 0, 0, 0.3  # Semi-transparent black

            )

            # Draw node background (main body)
            editor.draw_rectangle(
                self.x,
                self.y,
                self.width,
                self.height,
                self.secondary_color.red() / 255,
                self.secondary_color.green() / 255,
                self.secondary_color.blue() / 255
            )

            # Draw node header
            editor.draw_rectangle(
                self.x,
                self.y,
                self.width,
                self.header_size,
                self.primary_color.red() / 255,
                self.primary_color.green() / 255,
                self.primary_color.blue() / 255
            )

            if self.is_selected:
                editor.draw_rectangle_outline(
                    self.x - 15,
                    self.y - 15,
                    self.width + 30,
                    self.height + 30,
                    1, 1, 1, 0.2, 2
                )

            if self.is_over_header:
                editor.draw_rectangle(
                    self.x,
                    self.y,
                    self.width,
                    self.header_size,
                    1, 1, 1, 0.05
                )

            # Draw title text
            # Center the text vertically in the header
            text_x = self.x + 10  # Add some padding from the left
            text_y = self.y + (self.header_size / 2)  # Center point of header

            editor.draw_text(
                text_x,
                text_y,
                self.title,
                self.title_color.red() / 255,
                self.title_color.green() / 255,
                self.title_color.blue() / 255,
                1.0,
                self.title_font_size
            )

            # Render sockets
            socket_y = self.y + self.header_size
            for i, socket in enumerate(self.sockets):
                if socket.is_hovered:
                    editor.draw_rectangle(
                        self.x,
                        socket_y,
                        self.width,
                        socket.connected_height if socket.connections else socket.height,
                        1, 1, 1, 0.03
                    )
                if self.render_socket_regions:
                    clr_r = 1
                    clr_g = 0
                    clr_b = 0
                    if i % 2 == 1:
                        clr_r = 0
                        clr_g = 1
                        clr_b = 1
                    editor.draw_rectangle(
                        self.x,
                        socket_y,
                        self.width,
                        socket.height,
                        clr_r, clr_g, clr_b, 0.03
                    )

                socket.render_pin(self, self.x, socket_y, editor)
                show_interface = socket.check_show_interface()
                if show_interface:
                    socket_y += socket.height + self.sockets_spacing
                else:
                    socket_y += socket.connected_height + self.sockets_spacing

        def render_pass_connections():
            for socket in self.sockets:
                for connection in socket.connections:
                    connection: SocketConnection
                    from_node = connection.from_node
                    to_node = connection.to_node

                    from_socket = connection.from_socket
                    to_socket = connection.to_socket

                    prev_x, prev_y = from_node.get_socket_pos(from_socket)
                    prev_color = from_socket.pin_color
                    for reroute in connection.reroutes:
                        editor.draw_line(
                            prev_x, prev_y, reroute.x, reroute.y, 2, prev_color.red() / 255, prev_color.green() / 255, prev_color.blue() / 255, 1, reroute.color.red() / 255, reroute.color.green() / 255, reroute.color.blue() / 255, 1)
                        prev_x, prev_y = reroute.x, reroute.y
                        prev_color = reroute.color
                    editor.draw_line(
                        prev_x, prev_y, to_node.get_socket_pos(to_socket)[0], to_node.get_socket_pos(to_socket)[1], 2, prev_color.red() / 255, prev_color.green() / 255, prev_color.blue() / 255, 1, to_socket.pin_color.red() / 255, to_socket.pin_color.green() / 255, to_socket.pin_color.blue() / 255, 1)

        def render_pass_reroutes():
            for socket in self.sockets:
                for connection in socket.connections:
                    connection: SocketConnection
                    for reroute in connection.reroutes:
                        reroute.render(editor)

        editor.add_render_group(1, render_pass_connections)
        editor.add_render_group(2, render_pass_reroutes)
        editor.add_render_group(3, render_pass_node)

    def get_socket_x(self, socket: Socket):
        if socket.pin_type == "input":
            return self.x
        if socket.pin_type == "output":
            return self.x + self.width

    def get_socket_pos(self, socket: Socket):
        socket_y = self.y + self.header_size
        for current_socket in self.sockets:
            if current_socket == socket:
                return self.get_socket_x(current_socket), socket_y + current_socket.connected_height / 2
            show_interface = current_socket.check_show_interface()
            if show_interface:
                socket_y += current_socket.height + self.sockets_spacing
            else:
                socket_y += current_socket.connected_height + self.sockets_spacing


class NodeUtils:
    @classmethod
    def create_input_output_connection(cls, from_node: Node, from_socket: Socket, to_node: Node, to_socket: Socket):
        connection = SocketConnection()
        connection.from_node = from_node
        connection.from_socket = from_socket
        connection.to_node = to_node
        connection.to_socket = to_socket
        from_socket.connections.append(connection)
        to_socket.connections.append(connection)

    @classmethod
    def create_output_input_connection(cls, from_node: Node, from_socket: Socket, to_node: Node, to_socket: Socket):
        connection = SocketConnection()
        connection.from_node = from_node
        connection.from_socket = from_socket
        connection.to_node = to_node
        connection.to_socket = to_socket
        from_socket.connections.append(connection)
        to_socket.connections.append(connection)

    @classmethod
    def remove_connection(cls, connection: SocketConnection):
        connection.from_socket.connections.remove(connection)
        connection.to_socket.connections.remove(connection)

    @classmethod
    def check_line_intersection_with_connection(cls, line_start_x: float, line_start_y: float, line_end_x: float, line_end_y: float, connection: SocketConnection):
        # Checks if the line intersects with the connection while considering the connection's reroutes
        prev_x, prev_y = connection.from_node.get_socket_pos(
            connection.from_socket)

        # Check segments between reroutes
        for reroute in connection.reroutes:
            intersection_x, intersection_y = line_intersection(
                line_start_x, line_start_y, line_end_x, line_end_y,
                prev_x, prev_y, reroute.x, reroute.y
            )
            if intersection_x != False:
                return True
            prev_x, prev_y = reroute.x, reroute.y

        # Finally check segment to end socket
        if connection.to_node and connection.to_socket:
            to_x, to_y = connection.to_node.get_socket_pos(
                connection.to_socket)
            intersection_x, intersection_y = line_intersection(
                line_start_x, line_start_y, line_end_x, line_end_y,
                prev_x, prev_y, to_x, to_y
            )
            if intersection_x != False:
                return True

        return False

    @classmethod
    def get_intersections_with_connection(cls, line_start_x: float, line_start_y: float, line_end_x: float, line_end_y: float, connection: SocketConnection):
        intersections: list[tuple[float, float, int]] = []
        prev_x, prev_y = connection.from_node.get_socket_pos(
            connection.from_socket)

        # Check segments between reroutes
        reroute_index = 0
        for reroute in connection.reroutes:
            intersection_x, intersection_y = line_intersection(
                line_start_x, line_start_y, line_end_x, line_end_y,
                prev_x, prev_y, reroute.x, reroute.y
            )
            if intersection_x != False:
                intersections.append(
                    (intersection_x, intersection_y, reroute_index))
            prev_x, prev_y = reroute.x, reroute.y
            reroute_index += 1

        # Finally check segment to end socket
        if connection.to_node and connection.to_socket:
            to_x, to_y = connection.to_node.get_socket_pos(
                connection.to_socket)
            intersection_x, intersection_y = line_intersection(
                line_start_x, line_start_y, line_end_x, line_end_y,
                prev_x, prev_y, to_x, to_y
            )
            if intersection_x != False:
                intersections.append(
                    (intersection_x, intersection_y, reroute_index))

        return intersections
