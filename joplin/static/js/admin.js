document.addEventListener('DOMContentLoaded', function(event) {
  // HACK: I can't find a way to override this in python
  const title = document.querySelector('label[for=id_title]');
  if (title) {
    title.textContent = 'Actionable Title';
  }

  // HACK: I can't find a way to configure this to be closed via python
  document.querySelectorAll('#extra_content-prependmenu:not(.stream-menu-closed)').forEach((elem) => {
    elem.click();
  });
});
