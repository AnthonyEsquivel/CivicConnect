from django.test import TestCase

# Create your tests here.

from .models import Template, MyUser, User, Tags
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
    # does my template have no tags if I don't assign it any
    def testTemplateNoTags(self):
        a = Template(temp_name='ASPCA', temp_description='Help the Animals', temp_text='Dear Senator...')
        a.save()
        self.assertEquals(a.tags.all(),None)

class MyUser(TestCase):
    #Does MyUser address setup save to user
    def setUpMyUser(self):
         a=User(first_name="Shreyas")
         a.myuser = MyUser(address="1000 W Main Street", member_since=timezone.now())
         a.save()
         self.assertEquals(a.myUser.address, "1000 W Main Street")

    # Do tags get added to user's issues correctly
    def testUserIssues(self):
        t = Tags(name='Test Tag',id=100)
        t.save()
        a = User(first_name="User")
        a.myuser = MyUser(address="1000 W Main Street", member_since=timezone.now())
        a.myuser.save()
        a.save()
        a.myuser.issues.add(t)
        a.myuser.save()
        if t in a.myuser.issues.all():
            self.assertTrue
        else:
            self.assertFalse

    # does it throw an error when i put an invalid address
    def testInvalidAddress(self):
        a = User(first_name="Wendy")
        a.myuser = MyUser(address="!", member_since=timezone.now())
        try:
            a.save()
            error = False
        except IntegrityError:
            error = True
        self.assertTrue(error)
        
    # does my user create without a name
    def testMyUserNoName(self):
        a=User(first_name="Shreyas")
        a.myuser = MyUser()
        try:
            a.save()
            error = False
        except IntegrityError:
            error = True
        self.assertTrue(error)


class Tags(TestCase):
    # does my tag save to the database
    def setupTag(self):
        a = Tags(name='TESTTAG')
        a.save()
        self.assertEquals(a, Tags.objects.get(name='TESTTAG'))
    
    # Does the tag name work correctly
    def testTagCreation(self):
        tag = Tags(name='Test tag',id=100)
        tag.save()
        self.assertEquals(tag.name,'Test tag')

    # does my tag create without a name
    def testTagNoName(self):
        a = Tags()
        try:
            a.save()
            error = False
        except IntegrityError:
            error = True
        self.assertTrue(error)
    
