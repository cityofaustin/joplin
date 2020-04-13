$(function() {
  /**
    Our User form only knows about values for "Groups".
    So we need to parse the Groups that are set for that user,
    and set the values for "Roles" and "Departments" on the Form's UI.

    This code will only impact the "wagtailusers/users/edit" template.
    The "wagtailusers/users/create" template will not have existing Group data,
    because its creating a new user.

    Groups 1 and 2 are the "Editor" and "Moderator" groups.
    Those are selected by the "Roles" input checkbox fields.
    A Group larger than 2 will be a Department.
    That is selected by entering the value in the dropdown select field.
  **/
  const userGroupsRaw = $('#user-groups').text()
  if (userGroupsRaw) {
    const userGroups = JSON.parse(userGroupsRaw);
    userGroups.forEach(group => {
      if ([1,2].includes(group)) {
        $(`input[name='roles'][value=${group}]`).prop("checked", true)
      } else if (group > 2) {
        $("select[name='department']").val(group)
      }
    })
  }

  // Insert error messages into form
  const userErrorsRaw = $('#user-errors').text()
  if (userErrorsRaw) {
    const userErrors = JSON.parse(userErrorsRaw);
    if (userErrors.department) {
      const departmentParent = $($('label:contains("Department:")')[0]).parent()
      const departmentMessage = $(`<div class='coa-user-form-error'>${userErrors.department}</div>`)
      departmentMessage.insertBefore(departmentParent)
    }
    if (userErrors.roles) {
      const rolesParent = $($('label:contains("Roles:")')[0]).parent()
      const rolesMessage = $(`<div class='coa-user-form-error'>${userErrors.roles}</div>`)
      rolesMessage.insertBefore(rolesParent)
    }
  }
})
