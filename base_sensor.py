# micropython
# MIT license
# Copyright (c) 2022 Roman Shevchik   goctaprog@gmail.com
import micropython
import ustruct
import bus_service


@micropython.native
def check_value(value: int, valid_range, error_msg: str) -> int:
    if value not in valid_range:
        raise ValueError(error_msg)
    return value


class Device:
    """Base device class"""

    def __init__(self, adapter: bus_service.BusAdapter, address: int, big_byte_order: bool):
        """Базовый класс Устройство.
        Если big_byte_order равен True -> порядок байтов в регистрах устройства «big»
        (Порядок от старшего к младшему), в противном случае порядок байтов в регистрах "little"
        (Порядок от младшего к старшему)
        address - адрес устройства на шине.

        Base device class. if big_byte_order is True -> register values byteorder is 'big'
        else register values byteorder is 'little'
        address - address of the device on the bus."""
        self.adapter = adapter
        self.address = address
        self.big_byte_order = big_byte_order

    def _get_byteorder_as_str(self) -> tuple:
        """Return byteorder as string"""
        if self.is_big_byteorder():
            return 'big', '>'
        else:
            return 'little', '<'

    def unpack(self, fmt_char: str, source: bytes, redefine_byte_order: str = None) -> tuple:
        """распаковка массива, считанного из датчика.
        Если redefine_byte_order != None, то bo (смотри ниже) = redefine_byte_order
        fmt_char: c, b, B, h, H, i, I, l, L, q, Q. pls see: https://docs.python.org/3/library/struct.html"""
        if not fmt_char:
            raise ValueError(f"Invalid length fmt_char parameter: {len(fmt_char)}")
        bo = self._get_byteorder_as_str()[1]
        if redefine_byte_order is not None:
            bo = redefine_byte_order[0]
        return ustruct.unpack(bo + fmt_char, source)

    @micropython.native
    def is_big_byteorder(self) -> bool:
        return self.big_byte_order


class BaseSensor(Device):
    """Base sensor class"""
    def get_id(self):
        raise NotImplementedError

    def soft_reset(self):
        raise NotImplementedError


class Iterator:
    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError