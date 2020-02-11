from django.test import TestCase

'''
from wagtail group page permissions to keep in mind

class GroupPagePermission(models.Model):
    group = models.ForeignKey(Group, verbose_name=_('group'), related_name='page_permissions', on_delete=models.CASCADE)
    page = models.ForeignKey('Page', verbose_name=_('page'), related_name='group_permissions', on_delete=models.CASCADE)
    permission_type = models.CharField(
        verbose_name=_('permission type'),
        max_length=20,
        choices=PAGE_PERMISSION_TYPE_CHOICES
    )

    class Meta:
        unique_together = ('group', 'page', 'permission_type')
        verbose_name = _('group page permission')
        verbose_name_plural = _('group page permissions')

    def __str__(self):
        return "Group %d ('%s') has permission '%s' on page %d ('%s')" % (
            self.group.id, self.group,
            self.permission_type,
            self.page.id, self.page
        )
'''


# todo start actually writing these out

# Create your tests here.
class TestDepartmentPagePermissions(TestCase):
    def setUp(self):
        # Create some user accounts for testing permissions
        User = get_user_model()
        self.user = User.objects.create_user(username='user', email='user@email.com', password='password')
        self.owner = User.objects.create_user(username='owner', email='owner@email.com', password='password')
        self.editor = User.objects.create_user(username='editor', email='editor@email.com', password='password')
        self.editor.groups.add(Group.objects.get(name='Editors'))
        self.administrator = User.objects.create_superuser(
            username='administrator',
            email='administrator@email.com',
            password='password'
        )

        # Owner user must have the add_document permission
        self.adders_group = Group.objects.create(name='Document adders')
        GroupCollectionPermission.objects.create(
            group=self.adders_group, collection=Collection.get_first_root_node(),
            permission=Permission.objects.get(codename='add_document')
        )
        self.owner.groups.add(self.adders_group)

        # Create a document for running tests on
        self.document = models.Document.objects.create(title="Test document", uploaded_by_user=self.owner)

    def test_administrator_can_edit(self):
        self.assertTrue(self.document.is_editable_by_user(self.administrator))

    def test_editor_can_edit(self):
        self.assertTrue(self.document.is_editable_by_user(self.editor))

    def test_owner_can_edit(self):
        self.assertTrue(self.document.is_editable_by_user(self.owner))

    def test_user_cant_edit(self):
        self.assertFalse(self.document.is_editable_by_user(self.user))
