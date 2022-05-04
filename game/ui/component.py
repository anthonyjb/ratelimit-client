
class Component:
    """
    A base UI component.
    """

    def __init__(self):

        self._parent = None
        self._children = []

        self._tags = []

        self._event_listeners = {}

        self.bottom = None
        self.height = 5
        self.left = 0
        self.right = None
        self.top = 0
        self.width = 5
        self.z_index = 0

        self.enabled = True
        self.visible = True

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @property
    def rect(self):
        if not self.parent:
            return [self.top, self.left, self.height, self.width]

        parent_rect = self.parent.rect

        width = self.width
        if self.right is not None:
            width = parent_rect[3] - self.left - self.right

        height = self.height
        if self.bottom is not None:
            height = parent_rect[2] - self.top - self.bottom

        return [
            parent_rect[0] + self.top,
            parent_rect[1] + self.left,
            height,
            width
        ]

    @property
    def root(self):
        component = self
        while component.parent:
            component = component.parent
        return component

    @property
    def tags(self):
        return self._tags

    # Methods for managing children

    def add_child(self, child):
        """Add a child to the component"""
        self._children.append(child)
        child._parent = self

    def remove_child(self, child):
        """Remove a child from the component"""
        self._children.remove(child)
        child._parent = None

    # Methods for tagging/identifying components

    def add_tag(self, tag):
        """Add a tag to the component"""
        self._tags.append(tag)

    def closest(self, tag):
        """Return the closest ancestor with the given tag"""

        component = self
        while True:

            if tag in self.tags:
                return component

            component = component.parent
            if not component:
                break

    def one(self, tag):
        """Return the first descendent with the given tag"""

        for child in self.children:
            if tag in child.tags:
                return child

            descendent = child.one(tag)
            if descendent:
                return descendent

    def many(self, tag):
        """Return all descendents with the given tag"""

        descendents = []

        for child in self.children:
            if tag in child.tags:
                descendents.append(child)

            descendents += child.many(tag)

        return descendents

    def remove_tag(self, tag):
        """Remove a tag fomr the component"""
        self._tags.remove(tag)

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

    def render(self, ctx):
        """Render the UI component to the screen"""

        if self.visible:
            for child in sorted(self.children, key=lambda c: c.z_index):
                child.render(ctx)

    def update(self, dt):
        """
        Update the UI component based on the time ellapsed between now and the
        previous call to update.
        """

        if self.enabled:
            for child in self.children:
                child.update(dt)
