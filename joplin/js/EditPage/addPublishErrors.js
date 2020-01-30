const addFieldError = (field_name, messageElement) => {
  $(`label[for='id_${field_name}']`).parent().after(messageElement)
}

const addRelationError = (field_name, messageElement) => {
  $(messageElement).insertBefore($(`ul[id='id_${field_name}-FORMS']`).parent().parent())
}

const addStreamfieldError = () => {
}

/**
  Manually adds errors from PublishPreflight form validation.
  Builtin Wagtail error handling can't add errors to relations and streamfields.
  So we're going to do it manually.
**/
const addPublishErrors = () => {
  const publishErrors = JSON.parse(document.getElementById('publish-errors-data').textContent);
  if (publishErrors.length) {
    publishErrors.forEach((data, i)=>{
      const messageElement = `<div class='coa-publish-error'>${data.message}</div>`
      if (data.field_type === "field") {
        addFieldError(data.field_name, messageElement)
      } else if (data.field_type === "relation") {
        addRelationError(data.field_name, messageElement)
      } else if (data.field_type === "streamfield") {
        addStreamfieldError(data.field_name, messageElement)
      }
    })
  }
}

export default addPublishErrors;
