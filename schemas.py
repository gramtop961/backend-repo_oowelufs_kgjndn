"""
Database Schemas for Campus Karma Exchange

Each Pydantic model represents a collection in your MongoDB database.
Collection name is the lowercase of the class name (e.g., Pro -> "pro").
"""
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# Core domain schemas

class Pro(BaseModel):
    """
    Top student profiles offering help (service providers)
    Collection: "pro"
    """
    name: str = Field(..., description="Full name")
    avatar: Optional[str] = Field(None, description="Avatar URL")
    university: Optional[str] = Field(None, description="University or college")
    department: Optional[str] = Field(None, description="Department or major")
    bio: Optional[str] = Field(None, description="Short bio")
    tags: List[str] = Field(default_factory=list, description="Skill tags")
    rating: float = Field(4.5, ge=0, le=5, description="Average rating 0-5")
    reviews: int = Field(0, ge=0, description="Number of reviews")
    verified: bool = Field(False, description="Verified student status")
    karma_rate: int = Field(10, ge=0, description="Karma cost per session")

class Skill(BaseModel):
    """
    Skills a user can teach or trade
    Collection: "skill"
    """
    title: str
    category: str
    level: str = Field("Beginner", description="Beginner / Intermediate / Advanced")
    description: Optional[str] = None
    owner_name: Optional[str] = None
    featured: bool = False

class Request(BaseModel):
    """
    Help requests posted by students
    Collection: "request"
    """
    title: str
    details: Optional[str] = None
    category: str
    urgency: str = Field("Normal", description="Low / Normal / High")
    requester_name: Optional[str] = None
    offered_karma: int = Field(0, ge=0)
    status: str = Field("open", description="open / in_progress / completed")

# Optional user schema for future auth/profile work
class User(BaseModel):
    name: str
    email: EmailStr
    university: Optional[str] = None
    karma_balance: int = Field(0, ge=0)
    is_active: bool = True

