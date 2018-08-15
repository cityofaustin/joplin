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

  function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      var successful = document.execCommand("copy");
      var msg = successful ? "successful" : "unsuccessful";
      console.log("Fallback: Copying text command was " + msg);
    } catch (err) {
      console.error("Fallback: Oops, unable to copy", err);
    }

    document.body.removeChild(textArea);
  }

  function copyTextToClipboard(text) {
    if (!navigator.clipboard) {
      fallbackCopyTextToClipboard(text);
      return;
    }
    navigator.clipboard.writeText(text).then(
      function() {
        console.log("Async: Copying to clipboard was successful!");
      },
      function(err) {
        console.error("Async: Could not copy text: ", err);
      }
    );
  }

  var editform = $("#page-edit-form");
  var previewbutton = $("#page-preview-button");
  var sharebutton = $("#page-share-preview-button");
  var urlcopied = $("#page-share-url-copied");
  var messages = $(".messages");

  if (localStorage.previewing === "true") {
    window.open("{{preview_url}}", "_blank");
    localStorage.previewing = false;
  }

  if (localStorage.sharingpreview === "true") {
    // TODO: Don't just alert with the preview URL
    copyTextToClipboard("{{preview_url}}");
    urlcopied.removeClass("hidden");
    urlcopied.fadeOut(5000);
    localStorage.sharingpreview = false;
  }

  previewbutton.click(function() {
    localStorage.previewing = true;
  });

  sharebutton.click(function() {
    localStorage.sharingpreview = true;
  });

  messages.fadeOut(5000);
});
