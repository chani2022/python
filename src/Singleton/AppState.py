class AppState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppState, cls).__new__(cls, *args, **kwargs)
            cls._instance.next_position = 0
            cls._instance.count_stack = 0
            cls._instance.numero_acte = 1
        return cls._instance