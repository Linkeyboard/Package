from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'packages'
    pid = Column(Integer, primary_key=True)
    protocol = Column(String(50))
    num = Column(Integer)
    flow = Column(Integer)
    dst = Column(String(100))

    def __init__(self,pid=None, protocol=None, num=None, flow=None, dst=None):
        self.pid = pid
        self.protocol = protocol
        self.num = num
        self.flow = flow
        self.dst = dst 

    def __repr__(self):
        return '<id %r name %r>' % (self.openid,self.name)

