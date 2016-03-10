import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
  __tablename__ = 'restaurant'
  name = Column(String(80), nullable = False)
  id = Column(Integer, primary_key = True)

  @staticmethod
  def getAll(x):
    print x
