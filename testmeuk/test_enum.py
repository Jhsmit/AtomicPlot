from atom.api import Atom, Enum, Int, Str


class EnumTest(Atom):
    att = Enum(5, '4')




et = EnumTest()
et.att = 5
et.att = '5'
et.att = 3.4