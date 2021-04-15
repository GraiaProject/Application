Module graia.application.logger
===============================

Classes
-------

`AbstractLogger()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * graia.application.logger.LoggingLogger

    ### Methods

    `debug(self, msg)`
    :

    `error(self, msg)`
    :

    `exception(self, msg)`
    :

    `info(self, msg)`
    :

    `warn(self, msg)`
    :

`LoggingLogger(**kwargs)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * graia.application.logger.AbstractLogger
    * abc.ABC

    ### Methods

    `debug(self, msg)`
    :

    `error(self, msg)`
    :

    `exception(self, msg)`
    :

    `info(self, msg)`
    :

    `warn(self, msg)`
    :