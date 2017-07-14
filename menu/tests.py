from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime

from . import models


class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = models.Ingredient.objects.create(
            name='fish'
        )

    def test_creation(self):
        self.assertIn(self.ingredient, models.Ingredient.objects.all())

    def tearDown(self):
        self.ingredient.delete()


class ItemModelTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='Jay',
            email='test@example.com',
        )
        self.test_ingredient = models.Ingredient.objects.create(name='fish')
        self.item = models.Item.objects.create(
            name='grilled fish',
            description='put on fire and wait',
            chef=self.test_user
        )
        self.item.ingredients.add(self.test_ingredient)

    def test_creation(self):
        self.assertIn(self.item, models.Item.objects.all())

    def tearDown(self):
        self.item.delete()


class MenuModelTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='Jay',
            email='test@example.com',
        )
        self.test_ingredient = models.Ingredient.objects.create(name='fish')
        self.test_item = models.Item.objects.create(
            name='grilled fish',
            description='put on fire and wait',
            chef=self.test_user
        )
        self.test_item.ingredients.add(self.test_ingredient)
        self.menu = models.Menu.objects.create(
            season=1,
            year=2017,
            expiration_date=datetime.date.today()
        )
        self.menu.items.add(self.test_item)

    def test_creation(self):
        self.assertIn(self.menu, models.Menu.objects.all())

    def tearDown(self):
        self.menu.delete()


class MenuViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MenuViewTest, cls).setUpClass()
        test_user = User.objects.create_user(
            username='Jay',
            email='test@example.com',
        )
        test_ingredient = models.Ingredient.objects.create(name='fish')
        cls.item = models.Item.objects.create(
            name='grilled fish',
            description='put on fire and wait',
            chef=test_user
        )
        cls.item.ingredients.add(test_ingredient)
        cls.menu = models.Menu.objects.create(
            season=1,
            year=2017,
            expiration_date=datetime.date.today()
        )
        cls.menu.items.add(cls.item)

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, str(self.menu))
        menus = resp.context['menus']
        self.assertIn(self.menu, menus)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu_detail', kwargs={
                                                        'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, str(self.menu))
        menu = resp.context['menu']
        self.assertEqual(self.menu, menu)

    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail', kwargs={
                                                        'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, str(self.item))
        item = resp.context['item']
        self.assertEqual(self.item, item)

    def test_create_menu_view(self):
        resp = self.client.post(reverse('menu_new'), {
            'season': 2,
            'year': 2018,
            'expiration_date': datetime.date.today(),
            'items': [self.item.pk]
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        test_menu = models.Menu.objects.filter(season=2, year=2018).get()
        self.assertIsNotNone(test_menu)
        self.assertIn(self.item, test_menu.items.all())

    def test_edit_menu_view(self):
        expiration_date = self.menu.expiration_date + datetime.timedelta(
            days=5)
        resp = self.client.post(reverse('menu_edit', kwargs={
            'pk': self.menu.pk}), {
            'season': self.menu.season,
            'year': self.menu.year,
            'expiration_date': expiration_date,
            'items': self.menu.items.all().values_list('pk', flat=True)
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.expiration_date, expiration_date)
