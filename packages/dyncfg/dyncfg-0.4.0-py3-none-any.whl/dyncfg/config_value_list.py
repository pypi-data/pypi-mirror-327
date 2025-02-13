

class ConfigValueList:
    """A wrapper for a list of ConfigValue objects that supports method chaining.

    This class allows you to call methods on each element in the list in a chainable way.
    """

    def __init__(self, values):
        self.values = list(values)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, index):
        return self.values[index]

    def __repr__(self):
        return f"ConfigValueList({self.values!r})"

    def __getattr__(self, name):
        """Dynamically delegate attribute access to each ConfigValue in the list.

        If the invoked method returns a ConfigValue for every element, wrap the
        results in a new ConfigValueList for further chaining. Otherwise, return a list
        of results.
        """

        from dyncfg import ConfigValue

        def method(*args, **kwargs):

            results = [getattr(value, name)(*args, **kwargs) for value in self.values]
            # If all results are instances of ConfigValue, allow chaining.
            if all(isinstance(result, ConfigValue) for result in results):
                return ConfigValueList(results)
            else:
                return results  # Otherwise, simply return the list of results.

        return method
