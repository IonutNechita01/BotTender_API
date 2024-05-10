from pydantic import BaseModel, Field

class IngredientModel(BaseModel):
    name: str = Field(default='')
    position: int = Field(default=-1)
    id: str = Field(default='')
    imageUrl: str = Field(default='assets/images/ingredient_icon.png')
    barcode: str = Field(default='')
    type: str = Field(default='')
    subtype: str = Field(default='')
    quantity: float = Field(default=0.0)

    def toJson(self):
        return {
            "name": self.name,
            "position": self.position,
            "id": self.id,
            "imageUrl": self.imageUrl,
            "barcode": self.barcode,
            "type": self.type,
            "subtype": self.subtype,
            "quantity": self.quantity
        }

    @staticmethod
    def fromJson(json):
        return IngredientModel(
            name=json["name"],
            position=json["position"],
            id=json["id"],
            imageUrl=json["imageUrl"],
            barcode=json["barcode"],
            type=json["type"],
            subtype=json["subtype"],
            quantity=json["quantity"]
        )
