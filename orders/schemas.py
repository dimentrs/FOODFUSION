from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
  user_id: int
  description: str
  date: int
  cost: int
  status: str


class OrderCreate(OrderBase):
  pass


class OrderOut(OrderBase):
  model_config = ConfigDict(from_attributes=True)
  id: int

