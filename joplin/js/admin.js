// import '../css/admin.scss';

if (window.ISPRODUCTION !== "False") { // 🚨revert to simly `import '../joplin_UI/admin.scss'` after Joplin_UI is updated to prod
  require('../css/admin.scss');
} else if (localStorage.joplinUI !== "on") {
  require('../css/admin.scss');
} else {
  require('../joplin_UI/admin.scss');
}

$(function() {
  // HACK: I can't find a way to configure this to be closed via python
  document
    .querySelectorAll('#extra_content-prependmenu:not(.stream-menu-closed)')
    .forEach(elem => {
      elem.click();
    });
  var messages = $('.messages');
  messages.fadeOut(10000);
});
