import '../css/editor.scss';
import '../css/preview.scss';

import insertWizardData from './CreateContentModal/insertWizardData';
import menuActiveState from './EditPage/menuActiveState';
import toggleActivePanel from './SidebarPreview/toggleActivePanel';

$(function() {
  insertWizardData();
  menuActiveState();
  toggleActivePanel();

  // TODO: This a better way
  const anchors = {
    id_title: '#title',
    id_image: '#TODO',
    id_steps: '#steps',
    id_apps: '#apps',
    id_additional_content: '#additional',
    id_contacts: '#contacts',
    id_description: '#description',
    'id_process_steps-title': '#step-title',
    'id_process_steps-short_title': '#step-short-title',
    'id_process_steps-link_title': '#step-link-title',
    'id_process_steps-description': '#step-description',
    'id_process_steps-overview_steps': '#step-steps',
    'id_process_steps-detailed_content': '#step-details',
    'id_process_steps-quote': '#step-quote',
  };

  // Get all labels and add styleguide links
  const labels = document.querySelectorAll('label');
  const styleGuideUrl = document.getElementById('style_guide_url').value;

  for (const label of labels) {
    let id = label.getAttribute('for');

    // // Since we're getting these ids let's set the title text appropriately
    // if(id == "id_title") {
    //   // Super hack here, use the preview url to figure out what kind of page we're editing
    //   const previewRegex = /preview\/\w+\//g;
    //   const previewUrl = document.getElementById('preview_url').value;
    //   const previewTypeString = previewUrl.match(previewRegex)[0];
    //   if(previewTypeString == "preview/department/") {
    //     label.innerText = "Department Name"
    //   } else {
    //     label.innerText = "Write an actionable title"
    //   }
    // }

    // HACK: If we're dealing with subheadings in steps we need to remove the index
    if (id && id.includes('id_process_steps')) {
      const idTokens = id.split('-');
      id = `${idTokens[0]}-${idTokens[2]}`;
    }

    if (!id) {
      // HACK: Only some fields actually have for attributes
      switch (label.innerText) {
        case 'ADD ANY MAPS OR APPS THAT WILL HELP THE RESIDENT USE THE SERVICE ':
          id = 'id_apps';
          break;
        case 'CONTACTS':
          id = 'id_contacts';
          break;
        case 'PROCESS STEPS':
          id = 'id_steps';
          break;
      }
    }

    if (id in anchors) {
      var link = $('<a/>');
      link.addClass('icon-help-inverse');
      link.addClass('show');
      link.attr('href', `${styleGuideUrl}/${anchors[id]}`);
      link.attr('target', 'sidebar-iframe');
      $(label).append(link);
    }
  }

  $('.js-proxy-click').click(function() {
    let $this = $(this);
    $this.text($this.data('clicked-text'));

    let $button;

    let proxyByName = $this.data('proxyByName');
    if (proxyByName) {
      $button = $(`[name="${proxyByName}"]`);
    }

    let proxyByClass = $this.data('proxyByClass');
    if (proxyByClass) {
      $button = $(`.${proxyByClass}`);
    }

    if (!$button) {
      console.error(`Data attributes: ${$this.data()}`);
      throw new Error(
        'Unable to find a button. Did you specify data-proxy-by-name or data-proxy-by-class?',
      );
    }

    $button.click();
  });

  function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'successful' : 'unsuccessful';
      console.log('Fallback: Copying text command was ' + msg);
    } catch (err) {
      console.error('Fallback: Oops, unable to copy', err);
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
        console.log('Async: Copying to clipboard was successful!');
      },
      function(err) {
        console.error('Async: Could not copy text: ', err);
      },
    );
  }

  function changeLanguage(currentLang) {
    // Hide stuff that isn't our language
    // This is hacky but it seems to be working
    var languageStrings = {
      en: "[EN]",
      es: "[ES]",
      vi: "[VI]",
      ar: "[AR]"
    }

    var lowerLanguageStrings = {
      en: "[en]",
      es: "[es]",
      vi: "[vi]",
      ar: "[ar]"
    }

    var languageRegex = /\[\w+\]/g;

    document
      .querySelectorAll(".object")
      .forEach(elem => {
        if(elem.querySelectorAll("h2").length) {
          var headerText = elem.querySelectorAll("h2")[0].innerText;
          var langString = headerText.match(languageRegex);
          if (langString != null && langString != languageStrings[currentLang] && langString != lowerLanguageStrings[currentLang]) {
            elem.classList.add("hidden");
          } else {
            elem.classList.remove("hidden");
          }
        }
      });

    document
    .querySelectorAll(".field")
    .forEach(elem => {
      if(elem.querySelectorAll("label").length) {
        var labelText = elem.querySelectorAll("label")[0].innerText;
        var langString = labelText.match(languageRegex);
        
        if (langString != null && langString != lowerLanguageStrings[currentLang]) {
          elem.classList.add("hidden");
        } else {
          elem.classList.remove("hidden");
        }
      }
    });
  }

  var enButton = $('#en');
  enButton.click(function() {
    changeLanguage("en");
  });
  var esButton = $('#es');
  esButton.click(function() {
    changeLanguage("es");
  });
  var arButton = $('#ar');
  arButton.click(function() {
    changeLanguage("ar");
  });
  var viButton = $('#vi');
  viButton.click(function() {
    changeLanguage("vi");
  });

  changeLanguage("en");

  var editform = $('#page-edit-form');
  var previewbutton = $('#page-preview-button');
  var sharebutton = $('#page-share-preview-button');
  var urlcopied = $('#page-share-url-copied');
  var messages = $('.messages');

  const previewUrl = document.getElementById('preview_url').value;

  if (localStorage.previewing === 'true') {
    window.open(previewUrl, '_blank');
    localStorage.previewing = false;
  }

  if (localStorage.sharingpreview === 'true') {
    // TODO: Don't just alert with the preview URL
    copyTextToClipboard(previewUrl);
    urlcopied.removeClass('hidden');
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
