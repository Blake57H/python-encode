import json
from typing import Dict, Callable, Any, Type, Optional, Generic, TypeVar

_T = TypeVar('_T')


class DictReader:
    def __init__(self, dict_obj: Dict):
        if not isinstance(dict_obj, Dict):
            raise TypeError(f'Expected {type(Dict)}, got {type(dict_obj)}')
        self.dict_obj = dict_obj

    def set_from_val_read(self, set_func: Callable[[Any], Any], *dict_keys: str, defaults: Any = ...):
        reading_dict = json.loads(json.dumps(self.dict_obj))
        for dict_key in dict_keys:
            if not isinstance(reading_dict, dict):
                if defaults is not ...:
                    set_func(defaults)
                return
            reading_dict = reading_dict.get(dict_key, None)
            if reading_dict is None:
                if defaults is not ...:
                    set_func(defaults)
                return
        set_func(reading_dict)
        
    def read(self, *dict_keys: str, defaults: Any = None):
        reading_dict = json.loads(json.dumps(self.dict_obj))
        for dict_key in dict_keys:
            if not isinstance(reading_dict, dict):
                return defaults
            reading_dict = reading_dict.get(dict_key, None)
            if reading_dict is None:
                return defaults
        return reading_dict

    def create(self, type_obj, dict_key: str) -> Optional[object]:
        """I forgot what it was for..."""
        val = self.dict_obj.get(dict_key, None)
        if val is None:
            return None
        return type_obj.__new__(type_obj, val)


class GenericObject(Generic[_T]):
    _val: Optional["_T"] = None

    def __init__(self, init_val: Optional[_T] = None):
        self._val = init_val

    def get(self) -> Optional[_T]:
        return self._val

    def set(self, new_val: Optional[_T]):
        self._val = new_val


class Repository:
    pass