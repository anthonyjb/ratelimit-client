
class Event:
    """
    A class for creating UI events. UI events allow code to communicate with
    UI components.
    """

    def __init__(self, event_name, data=None):

        self._event_name = event_name

        self._origin_component = None
        self._component = None

        self._cancelled = False
        self._propagation_stopped = False

        self.data = data or {}

    def __copy__(self):
        event = Event(self.event_name, self.data)
        event._origin_component = self._origin_component
        event._cancelled = self._cancelled
        event._propagation_stopped = self._propagation_stopped
        return event

    @property
    def cancelled(self):
        return self._cancelled

    @property
    def component(self):
        return self._component

    @property
    def event_name(self):
        return self._event_name

    @property
    def origin_component(self):
        return self._origin_component

    @property
    def propagation_stopped(self):
        return self._propagation_stopped

    def cancel(self):
        """
        Cancel the event preventing associated listeners for the event being
        called after this point.
        """
        self._cancelled = True

    def stop_propagation(self):
        """
        Stop the event from propagating any higher (to parents beyond the
        this point).
        """
        self._propagation_stopped = True
