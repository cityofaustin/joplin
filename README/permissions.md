##Permissions
_last updated November 26, 2019_

Joplin has 3 groups: editors, moderators and administrators. 

Editors can 
  - View published content
  - Draft new content
  - Edit published content
  - View revision history
  - Replace current draft from revision history
  - Delete draft content they authored
  - View users
  - Add image
  - Edit image
  - Add Document
  - Edit Document

Moderators can do all that Editors can as well as
  - Publish / update content
  - Update from revision history
  - Unpublish content
  - Delete published content they authored
  - Delete content others authored
  - See and interact with the SEO tab
  - See and interact with the Content Settings tab
  - View snippet
  - Add Snippet
  - Save Publish Snippet
  - Delete images
  - Delete Documents

Admins can do all that Moderators can as well as
  - Delete snippets
  - Edit User
  - Add User
  - Delete User

Snippets are: 
  Contacts
  Locations
  Maps

To toggle the ability to modify snippets, you need to toggle the permissions for add, change, view and delete for each snippet model. 

###Wagtail Permissions

editors permissions: {'wagtaildocs.change_document', 'users.view_user', 'wagtaildocs.delete_document', 'wagtailimages.change_image', 'wagtailimages.add_image', 'wagtailimages.delete_image', 'wagtailadmin.access_admin', 'wagtaildocs.add_document'}

mods: 
{'base.add_location', 'base.change_map', 'wagtailimages.add_image', 'base.change_contact', 'base.view_map', 'base.view_snippets', 'wagtaildocs.add_document', 'base.view_contact', 'base.change_location', 'base.add_snippets', 'wagtaildocs.change_document', 'users.view_user', 'wagtaildocs.delete_document', 'wagtailimages.change_image', 'wagtailimages.delete_image', 'base.view_extra_panels', 'wagtailadmin.access_admin', 'base.add_map', 'base.add_contact', 'base.view_location'} 20


view_extra_panels - shows the SEO and setting tabs. see `janis_page.py`
view_snippets - shows the MenuItems in the admin menu. see `wagtail_hooks.py`



