class BaseConverter(object):
    def __init__(self, src_obj, Dst):
        self.src_obj = src_obj
        self.Dst = Dst

    def convert(self):
        return self.Dst()
