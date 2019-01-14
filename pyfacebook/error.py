class PyFacebookError(Exception):
    """ Base class for PyFacebook errors"""

    @property
    def message(self):
        """ return the error's first arg """
        return self.args[0]
