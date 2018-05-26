from sqlalchemy import Column, Integer, String
from database import Base

class Package(Base):
    __tablename__ = 'packages'
    pid = Column(Integer, primary_key=True, autoincrement = True)
    protocol = Column(String(50))
    num = Column(Integer)
    flow = Column(Integer)
    dst = Column(String(100))
    time = Column(String(100))

    def __init__(self, protocol=None, num=None, flow=None, dst=None, time=None):
        self.protocol = protocol
        self.num = num
        self.flow = flow
        self.dst = dst 
        self.time = time

        
    def __repr__(self):
        return '<id %r protocol %r num %r>' % (self.pid, self.protocol, self.num)

