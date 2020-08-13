$(function() {
  /**
    This code will fill out a User edit form with the correct existing values for a user.
    For example: if a user is part of the "Editors" group and part of the "Austin Public Health" department group,
    then this code fill in the checkbox next to "Editors" and select "Austin Public Health" from the department dropdown.

    Is is not done automatically because we created a custom user form that separates out the groups.

    The default User form only knows about values for "Groups".
    So we need to parse the Groups that are set for that user,
    and set the values for "Roles" and "Departments" on the Form's UI.

    This code will only impact the "wagtailusers/users/edit" template.
    The "wagtailusers/users/create" template will not have existing Group data,
    because its creating a new user.
  **/
  const userGroupsRaw = $('#user-groups').text()
  if (userGroupsRaw) {
    const userGroups = JSON.parse(userGroupsRaw);
    // Roles are selected by checkmarks
    userGroups.roles.forEach(group => {
      $(`input[name='roles'][value=${group}]`).prop("checked", true)
    })
    // Departmennt groups are selected by a dropdown
    userGroups.department_groups.forEach(group => {
      $("select[name='department']").val(group)
    })
    // Roles are selected by checkmarks
    userGroups.additional_groups.forEach(group => {
      $(`input[name='additional_groups'][value=${group}]`).prop("checked", true)
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
