import "../css/editor.scss";
import "../css/preview.scss";

$(function() {
  $(".js-proxy-click").click(function() {
    let $this = $(this);
    $this.text($this.data("clicked-text"));

    let $button;

    let proxyByName = $this.data("proxyByName");
    if (proxyByName) {
      $button = $(`[name="${proxyByName}"]`);
    }

    let proxyByClass = $this.data("proxyByClass");
    if (proxyByClass) {
      $button = $(`.${proxyByClass}`);
    }

    if (!$button) {
      console.error(`Data attributes: ${$this.data()}`);
      throw new Error(
        "Unable to find a button. Did you specify data-proxy-by-name or data-proxy-by-class?"
      );
    }

    $button.click();
  });
});
