# db/models.py
from sqlalchemy import (
    Column, Integer, String, Boolean, Float,
    ForeignKey, DateTime, Text, Table, Enum
)
from sqlalchemy.orm import relationship
import datetime
import enum
from .base import Base

# Enums
class AgeGroupEnum(str, enum.Enum):
    group_5_8 = "5-8"
    group_9_12 = "9-12"

class GenderEnum(str, enum.Enum):
    M = "M"
    F = "F"

# Join Table
kid_hard_letters = Table(
    'kid_hard_letters',
    Base.metadata,
    Column('kid_id', Integer, ForeignKey('kids.id'), primary_key=True),
    Column('letter_id', Integer, ForeignKey('hard_letters.id'), primary_key=True)
)

# Models (User, Kid, etc.)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    kids = relationship("Kid", back_populates="parent")

class Kid(Base):
    __tablename__ = 'kids'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    age_group = Column(Enum(AgeGroupEnum))
    gender = Column(Enum(GenderEnum))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    parent = relationship("User", back_populates="kids")
    hard_letters = relationship("HardLetter", secondary=kid_hard_letters, back_populates="kids")
    progresses = relationship("KidStoryProgress", back_populates="kid")

class HardLetter(Base):
    __tablename__ = 'hard_letters'
    id = Column(Integer, primary_key=True)
    letter = Column(String(1))
    kids = relationship("Kid", secondary=kid_hard_letters, back_populates="hard_letters")

class Story(Base):
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    cover_image = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    sentences = relationship("StorySentence", back_populates="story")

class StorySentence(Base):
    __tablename__ = 'story_sentences'
    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, ForeignKey('stories.id'))
    sentence = Column(Text)
    order_index = Column(Integer)
    audio_file = Column(String)
    story = relationship("Story", back_populates="sentences")

class KidStoryProgress(Base):
    __tablename__ = 'kid_story_progress'
    id = Column(Integer, primary_key=True)
    kid_id = Column(Integer, ForeignKey('kids.id'))
    story_id = Column(Integer, ForeignKey('stories.id'))
    current_sentence = Column(Integer)
    total_blocks = Column(Integer)
    total_repetitions = Column(Integer)
    completed = Column(Boolean)
    updated_at = Column(DateTime)
    kid = relationship("Kid", back_populates="progresses")
    speech_attempts = relationship("SpeechAttempt", back_populates="progress")

class Hint(Base):
    __tablename__ = 'hints'
    id = Column(Integer, primary_key=True)
    hint_text = Column(Text)
    hint_image = Column(String)
    category = Column(String)
    attempts = relationship("SpeechAttempt", back_populates="hint")

class SpeechAttempt(Base):
    __tablename__ = 'speech_attempts'
    id = Column(Integer, primary_key=True)
    progress_id = Column(Integer, ForeignKey('kid_story_progress.id'))
    sentence_id = Column(Integer, ForeignKey('story_sentences.id'))
    audio_path = Column(String)
    ai_score = Column(Float)
    blocks_count = Column(Integer)
    repetitions_count = Column(Integer)
    pauses_count = Column(Integer)
    hint_id = Column(Integer, ForeignKey('hints.id'))
    success = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    progress = relationship("KidStoryProgress", back_populates="speech_attempts")
    hint = relationship("Hint", back_populates="attempts")
