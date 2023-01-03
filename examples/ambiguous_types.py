class Preferences:
    def __init__(self) -> None:
        super().__init__()

    def func(self):
        pass

    def preferences(self):
        pass


class Utility:
    def __init__(self) -> None:
        pass

    def func(self):
        pass

    def utility(self):
        pass


class Meta:
    def __init__(self) -> None:
        pass

    def func(self):
        pass

    def meta(self):
        pass


def func():
    pass


# def call_preferences_and_utility():
#     preferences = Preferences()
#     utility = Utility()
#     preferences.func()
#     utility.func()


def call_preferences_and_meta():
    preferences = Preferences()
    meta = Meta()
    preferences.func()
    meta.func()


def call_utility():
    utility = Utility()
    utility.func()


def call_all_functions():
    Preferences.func()
    Utility.func()
    Meta.func()
    func()
