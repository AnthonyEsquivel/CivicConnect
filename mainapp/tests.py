from django.test import TestCase

# Create your tests here.

from .models import Template
from django.db.utils import IntegrityError


class TemplateModelTests(TestCase):
    # does my template save to the database
    def testTemplate(self):
        a = Template(temp_name='ASPCA', temp_description='Help the Animals', temp_text='Dear Senator...')
        a.save()
        self.assertEquals(a, Template.objects.get(temp_name='ASPCA'))

    # does my template create without a name
    def testTemplateNoName(self):
        a = Template(temp_name=None, temp_description='Help the Animals', temp_text='Dear Senator...')
        # try and let this happen, if there is an error that matches integrity error, i won't throw a big messy error
        # i will try to run the code inside the 'except' part
        try:
            a.save()
            error = False
        except IntegrityError:
            error = True
        self.assertTrue(error)





