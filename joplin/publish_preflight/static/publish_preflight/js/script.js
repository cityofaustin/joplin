$(function() {
  let messages = $('.messages');
  if (
    $('.messages')
      .children()
      .children()[0].className == !'error'
  ) {
    messages.fadeOut(10000);
  }
  if (
    $('.messages')
      .children()
      .children()[0].className == 'error'
  ) {
    messages.remove();
  }
});
