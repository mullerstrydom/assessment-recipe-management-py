from sqlmodel import Session


class IDatabaseConnection(object):
    def __init__(self):
        pass

    def get_session(self) -> Session:
        raise Exception("NotImplementedException")

    def close(self):
        raise Exception("NotImplementedException")
