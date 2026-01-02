from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Time, Date, BigInteger
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    name = Column(String, index=True)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Relationship to bookings
    bookings = relationship("Booking", back_populates="user")


class Service(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    duration = Column(Integer)  # in minutes
    price = Column(Integer)  # in cents or smallest currency unit
    description = Column(String, nullable=True)


class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    service_id = Column(Integer, ForeignKey('services.id'), nullable=True)
    date = Column(Date)
    time = Column(Time)
    duration = Column(Integer)  # in minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed = Column(Boolean, default=True)  # Auto-confirmed by default
    completed = Column(Boolean, default=False)
    canceled = Column(Boolean, default=False)
    
    # Relationship to user
    user = relationship("User", back_populates="bookings")
    # Relationship to service
    service = relationship("Service")


class Schedule(Base):
    __tablename__ = 'schedules'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    is_working_day = Column(Boolean, default=True)
    start_time = Column(Time, default='09:00:00')
    end_time = Column(Time, default='18:00:00')
    break_start = Column(Time, nullable=True)  # Optional break time
    break_end = Column(Time, nullable=True)    # Optional break end time
    created_at = Column(DateTime, default=datetime.utcnow)


class Waitlist(Base):
    __tablename__ = 'waitlist'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    service_id = Column(Integer, ForeignKey('services.id'), nullable=True)
    date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to user
    user = relationship("User")
    # Relationship to service
    service = relationship("Service")


class LoyaltyProgram(Base):
    __tablename__ = 'loyalty_program'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    visits_count = Column(Integer, default=0)
    discount_percentage = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to user
    user = relationship("User")