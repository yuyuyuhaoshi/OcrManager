class Configs:
    def __init__(self, config):
        super().__setattr__("_config", config)

    def set_property(self, name, value):
        self._config[name] = value

    def __getitem__(self, opt_name):
        opts = opt_name.split(".")
        if len(opts) > 1:
            result = self._config
            for opt in opts:
                opt = opt.upper()
                result = result[opt]
            return result
        if opt_name:
            opt_name = opt_name.upper()
        result = self._config
        return result[opt_name]

    def __setitem__(self, name, value):
        if name == "_config":
            self.__dict__[name] = value
        else:
            self.set_property(name, value)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


if __name__ == "__main__":
    c = Configs({})
    print(c["debug"])
    print(c.get("debug"))
