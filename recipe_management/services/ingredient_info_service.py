
class IngredientInfoService:

    def __init__(self):
        self.non_vegetarian_ingredients = [
            "Milk",
            "Cheese",
            "Butter",
            "Cream",
            "Yogurt",
            "Eggs",
            "Chicken",
            "Beef",
            "Pork",
            "Lamb",
            "Turkey",
            "Duck",
            "Bacon",
            "Ham",
            "Sausage",
            "Ground beef",
            "Chicken stock",
            "Beef stock",
            "Fish",
            "Salmon",
            "Tuna",
            "Shrimp",
            "Crab",
            "Anchovies",
            "Gelatin",
            "Lard"
        ]

    def is_vegetarian(self, ingredient_name: str) -> bool:
        return ingredient_name.lower() not in (name.lower() for name in self.non_vegetarian_ingredients)
