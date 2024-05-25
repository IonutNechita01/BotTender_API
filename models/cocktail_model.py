from pydantic import BaseModel, Field

class CocktailModel(BaseModel):
    name: str = Field(default='')
    id: str = Field(default='')
    imageUrl: str = Field(default='assets/images/ingredient_icon.png')
    ingredients: list = Field(default=[])

    def toJson(self):
        return {
            "name": self.name,
            "id": self.id,
            "imageUrl": self.imageUrl,
            "ingredients": self.ingredients
        }

    @staticmethod
    def fromJson(json):
        return CocktailModel(
            name=json["name"],
            id=json["id"],
            imageUrl=json["imageUrl"],
            ingredients=json["ingredients"]
        )
