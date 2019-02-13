from django.test import TestCase, Client

from shop.models import Category, Product

from django.test import tag


class SimpleTest(TestCase):
    """
    python manage.py test shop
    python manage.py test shop --tag=fast
    core, fast, slow
    """

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        """наполнение тестовой базы данных
        без данных база пустая
        setUpTestData - срабатывает первым"""
        Category.objects.create(name="Test1", slug="test1")
        Category.objects.create(name="Test2", slug="test2")
        Product.objects.create(
            category_id=1,
            title="Product-test1",
            description="Desc1",
            slug="product-test1")
        Product.objects.create(
            category_id=2,
            title="Product-test2",
            description="Desc2",
            slug="product-test2")

    @classmethod
    def tearDownClass(cls):
        """tearDownClass - срабатывает в конце тестирования"""
        print('конец тестирования')


    def test_category(self):
        """проверяю на точное совпадение строки"""
        category = Category.objects.get(slug="test1")
        self.assertEqual(category.name, "Test1")
        print(1)

    def test_category_exists(self):
        """проверка на наличие записи в бд"""
        category = Category.objects.filter(slug="test1")
        self.assertTrue(category.exists())
        print(2)

    def test_my(self):
        """проверка подстроки в тексте"""
        product = Product.objects.get(category__name__icontains="Test1")
        self.assertEqual(product.title, 'Product-test1')
        print(3)

    @tag('slow')
    def test_details(self):
        """проверка возвращаемого статуса кода"""
        response = self.client.get('/category-vue/')
        self.assertEqual(response.status_code, 200)
        # print(response.context)
        print(4)

    def test_cat_get(self):
        """вывод содержимого страницы"""
        response = self.client.get('/category/test1/')
        self.assertEqual(response.status_code, 200)
        # print(response.context["object_list"])
        print(5)


    @tag('fast')
    def test_cat_get(self):
        """вывод количества объектов на странице"""
        response = self.client.get('/')
        # Check that the rendered context contains 5 customers.
        self.assertEqual(len(response.context['object_list']), 2)
        print(6)
