# news/tests.py

from django.test import TestCase
from .models import Editor

class EditorTestClass(TestCase):

    # This method runs before every test
    def setUp(self):
        self.james = Editor(first_name='James', last_name='Muriuki', email='james@example.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.james, Editor))

    def test_save_method(self):
        self.james.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0)

    def test_delete_method(self):
        self.james.save_editor()
        self.james.delete()
        editors = Editor.objects.all()
        self.assertEqual(len(editors), 0)

    def test_update_editor(self):
        self.james.save_editor()
        editor = Editor.objects.get(email='james@example.com')
        editor.first_name = 'Jim'
        editor.save()
        updated = Editor.objects.get(email='james@example.com')
        self.assertEqual(updated.first_name, 'Jim')
