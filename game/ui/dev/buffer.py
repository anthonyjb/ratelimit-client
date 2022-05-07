
class Buffer(Component):
    """
    The Buffer UI component displays key value pairs and is designed to make
    it simpler during development post information (such as a variable value
    on screen).

    The buffer can be displayed or hidden using the home key. The buffer can
    contain more than one page of information, the page up / down keys can be
    used navigate between pages.
    """



#
# @@ START HERE
#
# - the buffer should exists as a default component in the UI root added as
#   part of the loop set up.
# - buffer can control it's visibility directly including setting it's z-index
#   to be a crazy high number (sys.maxsize) to ensure it always appears on top.
#
#

"""

________________________________________________________________________ 1 / 2
                                    |
Foo: Bar                            | Zee: Dee


"""


# ? WTF
#
# - why does calling fit_content in the parent to udpate a child send it all
#   over the place (buttons in info_panel).
#
