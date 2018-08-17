import "../css/editor.scss";
import "../css/preview.scss";

$(function() {
  // TODO: This a better way
  const anchors = {
    id_title: "#title",
    id_steps: "#steps",
    id_apps: "#apps",
    id_additional_content: "#additional",
    id_contacts: "#contacts",
    id_description: "#description",
    "id_process_steps-title": "#step-title",
    "id_process_steps-short_title": "#step-short-title",
    "id_process_steps-link_title": "#step-link-title",
    "id_process_steps-description": "#step-description",
    "id_process_steps-overview_steps": "#step-steps",
    "id_process_steps-detailed_content": "#step-details",
    "id_process_steps-quote": "#step-quote"
  };

  // Get all labels and add styleguide links
  const labels = document.querySelectorAll("label");
  const styleGuideUrl = document.getElementById("style_guide_url").value;

  for (const label of labels) {
    let id = label.getAttribute("for");

    // HACK: I can't find a way to override this in python
    if (id === "id_title") {
      label.textContent = "Actionable Title";
    }

    // HACK: If we're dealing with subheadings in steps we need to remove the index
    if (id && id.includes("id_process_steps")) {
      const idTokens = id.split("-");
      id = `${idTokens[0]}-${idTokens[2]}`;
    }

    if (!id) {
      // HACK: Only some fields actually have for attributes
      switch (label.innerText) {
        case "ADD ANY MAPS OR APPS THAT WILL HELP THE RESIDENT USE THE SERVICE ":
          id = "id_apps";
          break;
        case "CONTACTS":
          id = "id_contacts";
          break;
        case "PROCESS STEPS":
          id = "id_steps";
          break;
      }
    }

    if (id in anchors) {
      var link = $("<a/>");
      link.addClass("icon-help-inverse");
      link.addClass("show");
      link.attr("href", `${styleGuideUrl}/${anchors[id]}`);
      link.attr("target", "sidebar-iframe");
      $(label).append(link);
    }
  }

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
