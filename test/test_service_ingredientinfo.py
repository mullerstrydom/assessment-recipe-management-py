import unittest

from recipe_management.services.ingredient_info_service import IngredientInfoService


class IngredientInfoServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = IngredientInfoService()

    def test_is_vegetarian(self):
        ingredient_name = "Carrot"
        self.assertTrue(self.service.is_vegetarian(ingredient_name))


    def test_is_not_vegetarian(self):
        ingredient_name = "Bacon"
        self.assertFalse(self.service.is_vegetarian(ingredient_name))