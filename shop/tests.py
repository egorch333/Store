from django.test import TestCase, Client

from shop.models import Category, Product


class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        """наполнение тестовой базы данных
        без данных база пустая"""
        Category.objects.create(name="Test", slug="test")
        Product.objects.create(
            category_id=1,
            title="Product-test",
            description="Desc",
            slug="product-test")

    def test_category(self):
        """проверяю на точное совпадение строки"""
        category = Category.objects.get(slug="test")
        self.assertEqual(category.name, "Test")
        print(1)

    def test_category_exists(self):
        """проверка на наличие записи в бд"""
        category = Category.objects.filter(slug="test")
        self.assertTrue(category.exists())
        print(2)

    def test_my(self):
        """проверка подстроки в тексте"""
        product = Product.objects.get(category__name__icontains="Test")
        self.assertEqual(product.title, 'Product-test')
        print(3)

    def test_details(self):
        """проверка возвращаемого статуса кода"""
        response = self.client.get('/category-vue/')
        self.assertEqual(response.status_code, 200)
        # print(response.context)
        print(4)

    def test_cat_get(self):
        """вывод содержимого страницы"""
        response = self.client.get('/category/test/')
        self.assertEqual(response.status_code, 200)
        # print(response.context["object_list"])
        print(5)
