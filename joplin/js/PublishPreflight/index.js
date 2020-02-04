import './messages.scss';

// Removes multiple error messages that would pop up as a result of publish_preflight
$(function() {
  let messages = $(".messages");
  if (
    $(".messages")
      .children()
      .children()[0].className !== "error"
  ) {
    messages.fadeOut(10000);
  }
  if (
    $(".messages")
      .children()
      .children()[0].className == "error"
  ) {
    messages.remove();
  }
});
