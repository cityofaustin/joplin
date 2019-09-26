import '../css/editor.scss';
import '../css/preview.scss';

import insertWizardData from './CreateContentModal/insertWizardData';
import menuActiveState from './EditPage/menuActiveState';
import toggleActivePanel from './SidebarPreview/toggleActivePanel';
import richTextPlaceholder from './EditPage/richTextPlaceholder';

import _ from 'lodash';

$(function() {
  insertWizardData();
  menuActiveState();
  toggleActivePanel();
  richTextPlaceholder();

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
  const styleGuideUrl = djangoData.styleGuideUrl;

  // initialize state
  const state = {
    currentLang: 'en',
    janisPreviewUrl: getPreviewUrl('en'),
  };

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

  function getPreviewUrl(currentLang) {
    const previewUrlData = djangoData.previewUrlData;
    const janisUrlBase = previewUrlData.janis_url_base;
    const urlPageType = previewUrlData.url_page_type;
    const globalId = previewUrlData.global_id;
    let janisPreviewUrl = djangoData.fallBackPreviewUrl;
    if (janisUrlBase && urlPageType && globalId) {
      janisPreviewUrl = `${janisUrlBase}/${currentLang}/preview/${urlPageType}/${globalId}`;
    }
    return janisPreviewUrl;
  }

  // Changes language and update janisPreviewUrl for our language
  function changeLanguage(currentLang) {
    state.currentLang = currentLang;

    var languageStrings = {
      en: '[EN]',
      es: '[ES]',
      vi: '[VI]',
      ar: '[AR]',
    };

    var lowerLanguageStrings = {
      en: '[en]',
      es: '[es]',
      vi: '[vi]',
      ar: '[ar]',
    };

    var languageRegex = /\[\w+\]/g;

    // Hide stuff that isn't our language
    // This is hacky but it seems to be working

    // Top level fields
    document.querySelectorAll('.object').forEach(elem => {
      if (elem.querySelectorAll('.title-wrapper').length) {
        var headerText = elem.querySelectorAll('.title-wrapper')[0].innerText;
        var langString = headerText.match(languageRegex);
        if (
          langString != null &&
          langString != languageStrings[currentLang] &&
          langString != lowerLanguageStrings[currentLang]
        ) {
          elem.classList.add('hidden');
        } else {
          elem.classList.remove('hidden');
        }
      }
    });

    // Fields inside of InlinePanels
    document.querySelectorAll('.field').forEach(elem => {
      if (elem.querySelectorAll('label').length) {
        var labelText = elem.querySelectorAll('label')[0].innerText;
        var langString = labelText.match(languageRegex);

        if (
          langString != null &&
          langString != lowerLanguageStrings[currentLang]
        ) {
          elem.parentElement.classList.add('hidden');
        } else {
          elem.parentElement.classList.remove('hidden');
        }
      }
    });

    // Fields inside of Struct Blocks
    document.querySelectorAll('.struct-block').forEach(elem => {
      elem.querySelectorAll('label').forEach(label => {
        var labelText = label.innerText;
        var langString = labelText.match(languageRegex);

        if (
          langString != null &&
          langString != lowerLanguageStrings[currentLang]
        ) {
          label.parentElement.classList.add('hidden');
        } else {
          label.parentElement.classList.remove('hidden');
        }
      });
    });

    // Select language radio button if it isn't set already
    // For instance, if the language change is triggered by a refresh from clicking Share or Preview
    $(`#${currentLang}`).prop('checked', true);

    // ----
    // Switch the language for janisPreviewUrl
    // ----
    const janisPreviewUrl = getPreviewUrl(currentLang);
    state.janisPreviewUrl = janisPreviewUrl;

    const mobilePreviewSidebarButton = $('#mobile-preview-sidebar-button');
    const sharePreviewUrl = $('#share-preview-url');

    // Update link for "Mobile Preview" button on sidebar
    mobilePreviewSidebarButton.attr('href', janisPreviewUrl);
    sharePreviewUrl.text(janisPreviewUrl);

    // force reload of Mobile Preview iframe if its already open
    if (
      _.includes(
        mobilePreviewSidebarButton[0].classList,
        'coa-sidebar-button--active',
      )
    ) {
      $('#mobile-preview-iframe').attr('src', janisPreviewUrl);
    }
  }

  var enButton = $('#en');
  enButton.click(function() {
    changeLanguage('en');
  });
  var esButton = $('#es');
  esButton.click(function() {
    changeLanguage('es');
  });
  var arButton = $('#ar');
  arButton.click(function() {
    changeLanguage('ar');
  });
  var viButton = $('#vi');
  viButton.click(function() {
    changeLanguage('vi');
  });

  // When we add new fields to the page (orderable/streamfields etc.)
  // only show the appropriate fields based on language
  // we can do this by observing changes to our sections count

  $('#sections-count').change(function() {
    changeLanguage(state.currentLang);
  });

  // Found this here: https://stackoverflow.com/a/31719339
  MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

  var trackChange = function(element) {
    var observer = new MutationObserver(function(mutations, observer) {
      if (mutations[0].attributeName == 'value') {
        $(element).trigger('change');
      }
    });
    observer.observe(element, {
      attributes: true,
    });
  };

  // make sure observe all of them
  $('#sections-count').each(function(index, element) {
    trackChange(element);
  });

  // Initialize page in English, hide all other language fields
  changeLanguage('en');

  // Persist language for preview even after page refreshes on save
  var previewbutton = $('#page-preview-button');
  if (localStorage.preview_lang) {
    changeLanguage(localStorage.preview_lang);
    window.open(state.janisPreviewUrl, '_blank');
    localStorage.removeItem('preview_lang');
  }
  previewbutton.click(function() {
    localStorage.preview_lang = state.currentLang;
  });

  // Persist language for sharing even after page refreshes on save
  var sharebutton = $('#page-share-preview-button');
  var urlcopied = $('#page-share-url-copied');
  if (localStorage.share_lang) {
    // TODO: Don't just alert with the preview URL
    changeLanguage(localStorage.share_lang);
    copyTextToClipboard(state.janisPreviewUrl);
    urlcopied.removeClass('hidden');

    urlcopied.fadeOut(10000);
    localStorage.sharingpreview = false;
    localStorage.removeItem('share_lang');
  }
  sharebutton.click(function() {
    localStorage.share_lang = state.currentLang;
  });

  // Apply current language to new InlinePanels
  $('.add').click(function() {
    changeLanguage(state.currentLang);
  });

  var messages = $('.messages');
  messages.fadeOut(10000);
});
