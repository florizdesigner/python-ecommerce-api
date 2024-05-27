from pydantic import BaseModel, UUID4


class CreateOrder(BaseModel):
    description: str
    amount: int
    user_id: int


class Order(BaseModel):
    id: str
    description: str
    amount: int
    user_id: int

    def to_dict(self):
        return {"id": self.id, "description": self.description, "amount": self.amount, "user_id": self.user_id}