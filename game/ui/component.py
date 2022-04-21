
class Component:
    """
    A base UI component.
    """

    def __init__(self):

        self._parent = None
        self._children = []

        self._tags = []

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
    def extents(self):
        return [self.top, self.right, self.bottom, self.left]

    @extents.setter
    def extents(self, value):
        self.top = value[0]
        self.right = value[1]
        self.bottom = value[2]
        self.left = value[3]

    @property
    def height(self):
        return self.parent.height - self.top + self.bottom

    @height.setter
    def height(self, value):
        height = self.parent.height
        self.bottom = height - (height - self.top - value)

    @property
    def parent(self):
        return self._parent

    @property
    def root(self):
        component = self
        while component.parent:
            component = component.parent
        return component

    @property
    def tags(self):
        return self._tags

    @property
    def width(self):
        return self.parent.width - self.left + self.right

    @width.setter
    def width(self, value):
        width = self.parent.width
        self.right = width - (width - self.left - value)

    # Relative properties

    @property
    def rel_bottom(self):
        return self.rel_top + self.height

    @property
    def rel_extents(self):
        return [self.rel_top, self.rel_right, self.rel_bottom, self.rel_left]

    @property
    def rel_left(self):
        if self.parent:
            return self.parent.rel_left + self.left
        return self.left

    @property
    def rel_right(self):
        return self.rel_left + self.width

    @property
    def rel_top(self):
        if self.parent:
            return self.parent.rel_top + self.top
        return self.top

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


class FixedSizeComponent(Component):
    """
    A base UI component with a fixed width and height.
    """

    def __init__(self):
        super().__init__()

        self._width = 0
        self._height = 0

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
