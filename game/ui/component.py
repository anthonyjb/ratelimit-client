from game.ui.event import Event


class Component:
    """
    A base UI component.
    """

    def __init__(self):

        self._parent = None
        self._children = []

        self._event_listeners = {}

        self.bottom = 0
        self.left = 0
        self.top = 0
        self.right = 0
        self.z_index = 0

        self.enabled = True
        self.visible = True

    @property
    def children(self):
        return self._children

    @property
    def height(self):
        return self.parent.height - self.top - self.bottom

    @height.setter
    def height(self, value):
        height = self.parent.height
        self.bottom = height - (height - self.top - value)

    @property
    def parent(self):
        return self._parent

    @property
    def width(self):
        return self.parent.width - self.left - self.right

    @height.setter
    def width(self, value):
        width = self.parent.width
        self.right = height - (width - self.left - value)

    # Methods for managing children

    def addChild(self, child):
        """Add a child to the component"""
        self._children.append(child)
        child._parent = self

    def removeChild(self, child):
        """Remove a child to the component"""
        self._children.remove(child)
        child._parent = None

    # Methods for managing event handlers

    def add_event_listener(self, event_name, func):
        """Add an event listener for the named event for this component"""
        try:
            self._event_listeners[event_name].append(func)
        except KeyError:
            self._event_listeners[event_name] = [func]

    def dispatch_event(self, event):
        """Dispatch the given event against this component"""

        event = event.copy()
        event._origin_component = event.origin_component or self
        event._component = self

        if event.cancelled:

            for func in self._event_listeners.get(event_name, []):
                func(event)

            if not event.propagation_stopped and self.parent:
                self.parent.dispatch_event(event)

    def remove_event_listener(self, event_name, func):
        """Remove an event listener for the named event for this component"""
        if event_name in self._event_listeners:
            if func in self._event_listeners[event_name]:
                self._event_listeners[event_name].remove(func)

    # Lifecycle methods

    def input(self, char):
        """Handle the given user input for the UI component"""

        if self.enabled:
            for child in self.children:
                child.input(char)

    def render(self):
        """Render the UI component to the screen"""

        if self.visible:
            for child in self.children:
                child.render()

    def update(self, dt):
        """
        Update the UI component based on the time ellapsed between now and the
        previous call to update.
        """

        if self.enabled:
            for child in self.children:
                child.update(dt)
