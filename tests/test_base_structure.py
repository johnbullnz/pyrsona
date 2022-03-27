
from pyrsona import BaseStructure


class P(BaseStructure):
    pass


class C1(P):
    pass


class C11(C1):
    pass


class C12(C1):
    pass


class C2(P):
    pass


class C21(C2):
    pass


class C22(C2):
    pass


class C111(C11):
    pass


def test_get_structures():
    assert P.get_structures() == [C111, C11, C12, C1, C21, C22, C2, P]
    assert C1.get_structures() == [C111, C11, C12, C1]
    assert C11.get_structures() == [C111, C11]
    assert C12.get_structures() == [C12]


def test_read_data_from_file_encoding_utf8():
    data = BaseStructure._read_data_from_file("tests/data/utf8.txt")
    assert data == "utf-8"


def test_read_data_from_file_encoding_cp1252():
    data = BaseStructure._read_data_from_file("tests/data/cp1252.txt", encoding="cp1252")
    assert data == "cp1252 (\xf7)"
