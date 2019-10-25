import '../css/admin.scss';
import '../css/theme-override.scss';

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
