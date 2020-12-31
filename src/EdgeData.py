class EdgeData:

    def __init__(self, source_key: int, dest_key: int, weight: float):
        self._source_key = source_key
        self._dest_key = dest_key
        self._weight = weight
        self._info = "WHITE"
        self._tag = 0

    def get_src(self) -> int:
        return self._source_key

    def get_dest(self) -> int:
        return self._dest_key

    def get_weight(self) -> float:
        return self._weight

    def get_info(self) -> str:
        return self._info

    def set_info(self, info: str) -> None:
        self._info = str

    def get_tag(self) -> int:
        return self._tag

    def set_tag(self, tag: int) -> None:
        self._tag = tag

