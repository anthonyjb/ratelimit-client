"""
The settings module provides a shared `settings` instance that provides an
easy immutable way to access settings.
"""

import toml

__all__ = ('settings',)


class ReadOnlyDict(dict):

    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError
        return self.get(attr, None)

    def __setattr__(self, attr, value):
        raise TypeError('Settings cannot be set.')

    def __delattr__(self, attr):
        raise TypeError('Settings cannot be deleted.')


class Settings:

    def __init__(self):
        self.__dict__['_settings'] = {}

    def __getattr__(self, attr):
        self._load_settings(attr)
        return self.__dict__['_settings'][attr]

    def _load_settings(self, settings_name):

        if settings_name not in self.__dict__['_settings']:

            with open(f'cfg/{settings_name}.toml') as f:
                self.__dict__['_settings'][settings_name] \
                        = ReadOnlyDict(toml.load(f))


settings = Settings()

