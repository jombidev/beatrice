class Constants:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    __dic = {}

    def set(self, name: str, value):
        self.__dic[name] = value

    def add(self, name: str, value: int):
        if name not in self.__dic:
            self.__dic[name] = 0
        self.__dic[name] += value

    def get(self, name: str):
        if name not in self.__dic:
            raise ModuleNotFoundError(f'{name} not found on constants.')
        return self.__dic.get(name)
