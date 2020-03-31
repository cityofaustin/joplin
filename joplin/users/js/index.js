$(function() {
  const userGroups = JSON.parse(document.getElementById('user-groups').textContent);
  /**
    Our User form only knows about values for "Groups".
    So we need to parse the Groups that are set for that user,
    and set the values for "Roles" and "Departments" on the Form's UI.

    This only needs to be done for "wagtailusers/users/edit" template.
    The "wagtailusers/users/create" template will not have existing Group data,
    because its creating a new user.

    Groups 1 and 2 are the "Editor" and "Moderator" groups.
    Those are selected by the "Roles" input checkbox fields.
    A Group larger than 2 will be a Department.
    That is selected by entering the value in the dropdown select field.
  **/
  userGroups.forEach(group => {
    if ([1,2].includes(group)) {
      $(`input[name='roles'][value=${group}]`).prop("checked", true)
    } else if (group > 2) {
      $("select[name='department']").val(group)
    }
  })
})
