from .core import EclipseNodeEditor, node, Node, socket, Socket, tool, Tool, NodeUtils, Reroute, SocketConnection
from PyQt6.QtCore import Qt


class NodeMovingTool(Tool):
    def __init__(self):
        super().__init__()
        self.is_moving = False
        self.grabbed_reroute = None
        self.grabbed_connection = None
        self.start_mouse_x = 0
        self.start_mouse_y = 0

    def input(self, editor: EclipseNodeEditor):
        mouse_x, mouse_y = editor.get_mouse_pos()
        nodes = editor.get_objects_of_type(Node)

        if editor.left_mouse_pressed:
            if not editor.get_key(Qt.Key.Key_Shift):
                for node in nodes:
                    node: Node
                    node.is_selected = False
                    for socket in node.sockets:
                        socket: Socket
                        for connection in socket.connections:
                            connection: SocketConnection
                            for reroute in connection.reroutes:
                                reroute.is_selected = False

            # Check for Ctrl+left-click on reroutes
            if editor.get_key(Qt.Key.Key_Control):
                for node in nodes:
                    node: Node
                    for socket in node.sockets:
                        socket: Socket
                        for connection in socket.connections:
                            connection: SocketConnection
                            for reroute in connection.reroutes:
                                if reroute.is_hovered:
                                    editor.lock_tool(self)
                                    self.is_moving = True
                                    self.grabbed_reroute = reroute
                                    self.grabbed_connection = connection
                                    self.start_mouse_x = mouse_x
                                    self.start_mouse_y = mouse_y
                                    reroute.start_x = reroute.x
                                    reroute.start_y = reroute.y
                                    reroute.is_selected = True

                                    # Store initial positions of all selected nodes if shift is held
                                    if editor.get_key(Qt.Key.Key_Shift):
                                        for node in nodes:
                                            if node.is_selected:
                                                node.start_x = node.x
                                                node.start_y = node.y
                                                node.start_mouse_x = mouse_x
                                                node.start_mouse_y = mouse_y
                                    return

            # Regular node grabbing logic
            grabbed_node = editor.grabbed_object
            if isinstance(grabbed_node, Node):
                if grabbed_node.is_over_header:
                    editor.lock_tool(self)
                    self.is_moving = True
                    grabbed_node.start_mouse_x = mouse_x
                    grabbed_node.start_mouse_y = mouse_y
                    grabbed_node.start_x = grabbed_node.x
                    grabbed_node.start_y = grabbed_node.y
                    grabbed_node.is_selected = True

        if self.is_moving:
            if editor.left_mouse_down:
                # Handle reroute movement
                if self.grabbed_reroute:
                    dx = mouse_x - self.start_mouse_x
                    dy = mouse_y - self.start_mouse_y
                    # Move all selected reroutes
                    for node in nodes:
                        # If shift is held, also move selected nodes
                        if editor.get_key(Qt.Key.Key_Shift):
                            if node.is_selected:
                                node.x = node.start_x + dx
                                node.y = node.start_y + dy

                        for socket in node.sockets:
                            for connection in socket.connections:
                                for reroute in connection.reroutes:
                                    if reroute.is_selected:
                                        reroute.x = reroute.start_x + dx
                                        reroute.y = reroute.start_y + dy
                else:
                    # Handle node movement
                    reroutes = set()
                    if editor.grabbed_object:
                        if isinstance(editor.grabbed_object, Node):
                            for obj in nodes:
                                obj: Node
                                if obj.is_selected:
                                    obj.x = obj.start_x + mouse_x - editor.grabbed_object.start_mouse_x
                                    obj.y = obj.start_y + mouse_y - editor.grabbed_object.start_mouse_y

                                for socket in obj.sockets:
                                    socket: Socket
                                    for connection in socket.connections:
                                        connection: SocketConnection
                                        for reroute in connection.reroutes:
                                            if reroute.is_selected:
                                                if reroute not in reroutes:
                                                    reroutes.add(reroute)
                                                    reroute.x = reroute.start_x + mouse_x - editor.grabbed_object.start_mouse_x
                                                    reroute.y = reroute.start_y + mouse_y - editor.grabbed_object.start_mouse_y

        if editor.left_mouse_released:
            self.is_moving = False
            self.grabbed_reroute = None
            self.grabbed_connection = None
            for node in nodes:
                node: Node
                node.start_mouse_x = mouse_x
                node.start_mouse_y = mouse_y
                node.start_x = node.x
                node.start_y = node.y

                for socket in node.sockets:
                    socket: Socket
                    for connection in socket.connections:
                        connection: SocketConnection
                        for reroute in connection.reroutes:
                            reroute.start_x = reroute.x
                            reroute.start_y = reroute.y

            editor.unlock_tool()


class SelectingTool(Tool):
    def __init__(self):
        super().__init__()
        self.is_selecting = False
        self.start_mouse_x = 0
        self.start_mouse_y = 0
        self.already_selected_nodes: list[Node] = []
        self.already_selected_reroutes: set[Reroute] = set()

    def setup(self, editor: EclipseNodeEditor):
        """Setup the tool's input bindings"""
        editor.register_binding(
            "selecting",
            201,  # Base priority for right-click
            lambda: editor.left_mouse_pressed and editor.get_key(
                Qt.Key.Key_Shift),
            "Select nodes with left-click"
        )

    def input(self, editor: EclipseNodeEditor):
        mouse_x, mouse_y = editor.get_mouse_pos()
        if editor.get_binding("selecting"):
            editor.lock_tool(self)
            self.is_selecting = True
            self.start_mouse_x = mouse_x
            self.start_mouse_y = mouse_y
            self.already_selected_nodes = []
            self.already_selected_reroutes = set()
            nodes = editor.get_objects_of_type(Node)
            for node in nodes:
                node: Node
                if node.is_selected:
                    self.already_selected_nodes.append(node)

                for socket in node.sockets:
                    socket: Socket
                    for connection in socket.connections:
                        connection: SocketConnection
                        for reroute in connection.reroutes:
                            if reroute.is_selected:
                                self.already_selected_reroutes.add(reroute)

        if self.is_selecting:
            if editor.left_mouse_down:
                nodes = editor.get_objects_of_type(Node)
                # Calculate selection bounds regardless of drag direction
                min_x = min(self.start_mouse_x, mouse_x)
                max_x = max(self.start_mouse_x, mouse_x)
                min_y = min(self.start_mouse_y, mouse_y)
                max_y = max(self.start_mouse_y, mouse_y)

                for node in nodes:
                    node: Node
                    # Check if node overlaps with selection rectangle
                    node_left = node.x
                    node_right = node.x + node.width
                    node_top = node.y
                    node_bottom = node.y + node.height

                    # Check for overlap in both axes
                    overlap_x = (node_left < max_x) and (node_right > min_x)
                    overlap_y = (node_top < max_y) and (node_bottom > min_y)

                    if node not in self.already_selected_nodes:
                        if overlap_x and overlap_y:
                            node.is_selected = True
                        else:
                            node.is_selected = False

                    for socket in node.sockets:
                        socket: Socket
                        for connection in socket.connections:
                            connection: SocketConnection
                            for reroute in connection.reroutes:
                                if reroute not in self.already_selected_reroutes:
                                    if reroute.x >= min_x and reroute.x <= max_x and reroute.y >= min_y and reroute.y <= max_y:
                                        reroute.is_selected = True
                                    else:
                                        reroute.is_selected = False

        if editor.left_mouse_released:
            self.is_selecting = False
            editor.unlock_tool()
            editor.clear_active_binding()
            self.already_selected_nodes = []
            self.already_selected_reroutes = set()

    def render(self, editor: EclipseNodeEditor):
        if self.is_selecting:
            def render_selecting_rectangle():
                mouse_x, mouse_y = editor.get_mouse_pos()
                # Calculate rectangle dimensions regardless of drag direction
                rect_x = min(self.start_mouse_x, mouse_x)
                rect_y = min(self.start_mouse_y, mouse_y)
                rect_width = abs(mouse_x - self.start_mouse_x)
                rect_height = abs(mouse_y - self.start_mouse_y)

                editor.draw_rectangle(
                    rect_x, rect_y, rect_width, rect_height,
                    0.08, 0.51, 0.86, 0.1
                )

                editor.draw_rectangle_outline(
                    rect_x, rect_y, rect_width, rect_height,
                    0.08, 0.51, 0.86, 0.7, 2
                )

            editor.add_render_group(100, render_selecting_rectangle)


class NodeConnectionTool(Tool):
    def __init__(self):
        super().__init__()
        self.from_node_and_socket: tuple[Node, Socket] | None = None
        self.to_node_and_socket: tuple[Node, Socket] | None = None
        self.from_reroute: tuple[Reroute, SocketConnection] | None = None
        self.to_reroute: tuple[Reroute, SocketConnection] | None = None

    def check_connection_exists(self, socket1: Socket, socket2: Socket) -> bool:
        """Check if a connection already exists between these two sockets"""
        for connection in socket1.connections:
            if (connection.from_socket == socket1 and connection.to_socket == socket2) or \
               (connection.from_socket == socket2 and connection.to_socket == socket1):
                return True
        return False

    def input(self, editor: EclipseNodeEditor):
        mouse_x, mouse_y = editor.get_mouse_pos()

        if editor.left_mouse_pressed:
            nodes = editor.get_objects_of_type(Node)
            self.from_node_and_socket = None
            self.from_reroute = None

            # First check for reroute clicks
            for node in nodes:
                node: Node
                for socket in node.sockets:
                    for connection in socket.connections:
                        for reroute in connection.reroutes:
                            if reroute.is_hovered:
                                self.from_reroute = (reroute, connection)
                                editor.lock_tool(self)
                                return

            # Then check for socket clicks
            for node in reversed(nodes):
                node: Node
                for socket in node.sockets:
                    if socket.is_pin_hovered:
                        self.from_node_and_socket = (node, socket)
                        editor.lock_tool(self)
                        break

        if self.from_node_and_socket or self.from_reroute:
            if editor.left_mouse_released:
                nodes = editor.get_objects_of_type(Node)
                self.to_node_and_socket = None
                self.to_reroute = None

                # First check for reroute clicks
                for node in nodes:
                    node: Node
                    for socket in node.sockets:
                        for connection in socket.connections:
                            for reroute in connection.reroutes:
                                if reroute.is_hovered:
                                    self.to_reroute = (reroute, connection)
                                    break

                # Then check for socket clicks if no reroute was clicked
                if not self.to_reroute:
                    for node in reversed(nodes):
                        node: Node
                        for socket in node.sockets:
                            if socket.is_pin_hovered:
                                self.to_node_and_socket = (node, socket)
                                break

                # Handle the different connection cases
                if self.from_node_and_socket:
                    from_node, from_socket = self.from_node_and_socket

                    # Socket to Socket
                    if self.to_node_and_socket:
                        to_node, to_socket = self.to_node_and_socket
                        if from_node != to_node:  # Don't connect to same node
                            if not self.check_connection_exists(from_socket, to_socket):
                                if from_socket.pin_type == "input" and to_socket.pin_type == "output":
                                    NodeUtils.create_input_output_connection(
                                        to_node, to_socket, from_node, from_socket)
                                elif from_socket.pin_type == "output" and to_socket.pin_type == "input":
                                    NodeUtils.create_output_input_connection(
                                        from_node, from_socket, to_node, to_socket)

                    # Socket to Reroute
                    elif self.to_reroute:
                        reroute, connection = self.to_reroute
                        # Find reroute index
                        reroute_index = connection.reroutes.index(reroute)

                        # If connecting output to reroute
                        if from_socket.pin_type == "output":
                            # Check if connection already exists
                            if not self.check_connection_exists(from_socket, connection.to_socket):
                                # Create new connection from output to input
                                new_connection = SocketConnection()
                                new_connection.from_node = from_node
                                new_connection.from_socket = from_socket
                                new_connection.to_node = connection.to_node
                                new_connection.to_socket = connection.to_socket
                                # Include reroutes at and after the clicked one
                                new_connection.reroutes = connection.reroutes[reroute_index:]
                                from_socket.connections.append(new_connection)
                                connection.to_socket.connections.append(
                                    new_connection)

                        # If connecting input to reroute
                        elif from_socket.pin_type == "input":
                            # Check if connection already exists
                            if not self.check_connection_exists(from_socket, connection.from_socket):
                                # Create new connection from output to input
                                new_connection = SocketConnection()
                                new_connection.from_node = connection.from_node
                                new_connection.from_socket = connection.from_socket
                                new_connection.to_node = from_node
                                new_connection.to_socket = from_socket
                                # Include reroutes up to and including the clicked one
                                new_connection.reroutes = connection.reroutes[:reroute_index + 1]
                                connection.from_socket.connections.append(
                                    new_connection)
                                from_socket.connections.append(new_connection)

                elif self.from_reroute:
                    reroute, connection = self.from_reroute
                    reroute_index = connection.reroutes.index(reroute)

                    # Reroute to Socket
                    if self.to_node_and_socket:
                        to_node, to_socket = self.to_node_and_socket
                        if to_socket.pin_type == "input":
                            # Check if connection already exists
                            if not self.check_connection_exists(connection.from_socket, to_socket):
                                # Create new connection from output to input
                                new_connection = SocketConnection()
                                new_connection.from_node = connection.from_node
                                new_connection.from_socket = connection.from_socket
                                new_connection.to_node = to_node
                                new_connection.to_socket = to_socket
                                # Include reroutes up to and including the clicked one
                                new_connection.reroutes = connection.reroutes[:reroute_index + 1]
                                connection.from_socket.connections.append(
                                    new_connection)
                                to_socket.connections.append(new_connection)

                # Reset state
                self.from_node_and_socket = None
                self.to_node_and_socket = None
                self.from_reroute = None
                self.to_reroute = None

        if editor.left_mouse_released:
            editor.unlock_tool()

    def render(self, editor: EclipseNodeEditor):
        def render_temp_connection():
            mouse_x, mouse_y = editor.get_mouse_pos()
            if self.from_node_and_socket:
                from_node, from_socket = self.from_node_and_socket
                socket_x, socket_y = from_node.get_socket_pos(from_socket)
                editor.draw_line(socket_x, socket_y, mouse_x,
                                 mouse_y, 2, 1, 1, 1, 1)
            elif self.from_reroute:
                reroute, _ = self.from_reroute
                editor.draw_line(reroute.x, reroute.y, mouse_x,
                                 mouse_y, 2, 1, 1, 1, 1)

        editor.add_render_group(10, render_temp_connection)


class ConnectionCuttingTool(Tool):
    def __init__(self):
        super().__init__()
        self.start_mouse_x = 0
        self.start_mouse_y = 0
        self.is_cutting = False
        # connection is the key, intersections is the value
        self.connections_to_cut_data: dict[SocketConnection,
                                           list[tuple[float, float]]] = {}

    def setup(self, editor: EclipseNodeEditor):
        """Setup the tool's input bindings"""
        editor.register_binding(
            "connection_cut",
            200,  # Base priority for right-click
            lambda: editor.right_mouse_pressed and editor.get_key(
                Qt.Key.Key_Shift),
            "Cut connections"
        )

    def input(self, editor: EclipseNodeEditor):
        mouse_x, mouse_y = editor.get_mouse_pos()

        if editor.get_binding("connection_cut"):
            editor.lock_tool(self)
            self.start_mouse_x = mouse_x
            self.start_mouse_y = mouse_y
            self.is_cutting = True

        if editor.right_mouse_down:
            self.update_connection_data(editor)

        if editor.right_mouse_released:
            self.is_cutting = False
            self.update_connection_data(editor)
            for connection, intersections in self.connections_to_cut_data.items():
                if len(intersections) > 0:
                    NodeUtils.remove_connection(connection)
            editor.unlock_tool()
            editor.clear_active_binding()

    def update_connection_data(self, editor: EclipseNodeEditor):
        self.connections_to_cut_data = {}
        mouse_x, mouse_y = editor.get_mouse_pos()
        nodes = editor.get_objects_of_type(Node)
        for node in nodes:
            node: Node
            for socket in node.sockets:
                for connection in socket.connections:
                    intersections = NodeUtils.get_intersections_with_connection(
                        self.start_mouse_x, self.start_mouse_y, mouse_x, mouse_y, connection)
                    if intersections:
                        self.connections_to_cut_data[connection] = intersections

    def render(self, editor: EclipseNodeEditor):
        def render_cutting_line():
            if self.is_cutting:
                mouse_x, mouse_y = editor.get_mouse_pos()
                editor.draw_line(self.start_mouse_x, self.start_mouse_y, mouse_x,
                                 mouse_y, 2, 1, 0, 0, 1)

                for connection, intersections in self.connections_to_cut_data.items():
                    for intersection in intersections:
                        editor.draw_circle(
                            intersection[0], intersection[1], 5, 1, 0, 0, 1)

        editor.add_render_group(100, render_cutting_line)


class ConnectionRerouteTool(Tool):
    def __init__(self):
        super().__init__()
        self.start_mouse_x = 0
        self.start_mouse_y = 0
        self.is_rerouting = False
        # connection is the key, intersections is the value
        self.connections_to_reroute_data: dict[SocketConnection,
                                               list[tuple[float, float]]] = {}

    def setup(self, editor: EclipseNodeEditor):
        """Setup the tool's input bindings"""
        editor.register_binding(
            "connection_reroute",
            100,  # Higher priority than cut for shift+right-click
            lambda: editor.right_mouse_pressed,
            "Reroute connections"
        )

    def input(self, editor: EclipseNodeEditor):
        mouse_x, mouse_y = editor.get_mouse_pos()

        if editor.get_binding("connection_reroute"):
            editor.lock_tool(self)
            self.start_mouse_x = mouse_x
            self.start_mouse_y = mouse_y
            self.is_rerouting = True

        if editor.right_mouse_down:
            self.update_connection_data(editor)

        if editor.right_mouse_released:
            self.is_rerouting = False
            self.update_connection_data(editor)
            for connection, intersections in self.connections_to_reroute_data.items():
                if len(intersections) > 0:
                    # Sort intersections by index to maintain correct order
                    sorted_intersections = sorted(
                        intersections, key=lambda x: x[2])
                    # Add all reroutes, adjusting indices as we insert
                    offset = 0
                    for x, y, index in sorted_intersections:
                        # Insert at the original index plus offset from previous insertions
                        new_reroute = Reroute(x, y)
                        new_reroute.color = connection.from_socket.pin_color
                        connection.reroutes.insert(index + offset, new_reroute)
                        offset += 1
            editor.unlock_tool()
            editor.clear_active_binding()

    def update_connection_data(self, editor: EclipseNodeEditor):
        self.connections_to_reroute_data = {}
        mouse_x, mouse_y = editor.get_mouse_pos()
        nodes = editor.get_objects_of_type(Node)
        for node in nodes:
            node: Node
            for socket in node.sockets:
                for connection in socket.connections:
                    intersections = NodeUtils.get_intersections_with_connection(
                        self.start_mouse_x, self.start_mouse_y, mouse_x, mouse_y, connection)
                    if intersections:
                        self.connections_to_reroute_data[connection] = intersections

    def render(self, editor: EclipseNodeEditor):
        def render_rerouting_line():
            if self.is_rerouting:
                mouse_x, mouse_y = editor.get_mouse_pos()
                editor.draw_line(self.start_mouse_x, self.start_mouse_y, mouse_x,
                                 mouse_y, 2, 0, 1, 1, 1)

                for connection, intersections in self.connections_to_reroute_data.items():
                    for intersection in intersections:
                        editor.draw_circle(
                            intersection[0], intersection[1], 5, 0, 1, 1, 1)

        editor.add_render_group(100, render_rerouting_line)


@node()
class TestNode(Node):
    def __init__(self, x, y, title):
        super().__init__(x, y, title)
        self.add_input_socket(Socket())
        self.add_output_socket(Socket())
