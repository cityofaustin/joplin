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

  var language = document.getElementById('language-select-wrapper');
  var content = document.getElementsByClassName('tab-nav merged')[0]
    .firstElementChild;
  content.appendChild(language);

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
  // TODO: what is this for??
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

  // TODO; verify this code is still used, move to into a utilities section
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
    const janisPreviewUrlStart = previewUrlData.janis_preview_url_start;
    const janisPreviewUrlEnd = previewUrlData.janis_preview_url_end;
    return `${janisPreviewUrlStart}/${currentLang}/${janisPreviewUrlEnd}`;
  }

  function setTabToContent() {
    $('.tab-nav a')
      .first()
      .tab('show');
    window.history.replaceState(
      null,
      null,
      $('.tab-nav a')
        .first()
        .attr('href'),
    );
  }
  // Changes language and update janisPreviewUrl for our language
  function changeLanguage(currentLang) {
    state.currentLang = currentLang;
    setTabToContent();

    // replace brackets with hidden span tags
    function replaceLanguageLabels() {
      const languageLabels = $('ul[class="objects"]').find(
        'label:contains(" [")',
      );
      if (languageLabels.length) {
        if (typeof state.languageLabels === 'undefined') {
          state.languageLabels = languageLabels;
        } else {
          for (let label in languageLabels) {
            state.languageLabels.push(languageLabels[label]);
          }
        }
        languageLabels.each(function() {
          this.innerHTML = this.innerHTML.replace(
            '[',
            " <span style='display:none;'>",
          );
          this.innerHTML = this.innerHTML.replace(']', '</span>');
        });
      }
    }
    replaceLanguageLabels();

    // TODO: refactor into a function, evaluate performance
    // have better variable namepsace seperation
    let labelList = state.languageLabels;
    for (let label in labelList) {
      if (labelList[label].querySelector) {
        let languageTag = labelList[label].querySelector('span').innerText;
        // these seem to be nested twice, from the title to the containing element
        // TODO: come up with a more elegant and maintable way to check what elements ought to be hidden
        if (
          labelList[label].parentElement.parentElement.parentElement.classList
            .value !== 'struct-block'
        ) {
          const translatedElement = labelList[label].parentElement.parentElement;

          if (languageTag != null && languageTag != currentLang) {
            translatedElement.classList.add('hidden');
          } else {
            translatedElement.classList.remove('hidden');
          }
          /*  While the first condition checks for 'struct-blocks' with language tags,
              it doesn't catch the case where there are 'struct-blocks' with language
              tages WITHIN the element itself. The following condition checks for those conditions.
              - The was neccessary for guide stream fields. */
          if (translatedElement.classList.contains("struct-block")) {
            const fieldlabels = translatedElement.querySelectorAll('[for]')
            fieldlabels.forEach( fieldlabel => {
              const attrFor = fieldlabel.getAttribute('for').split("_")
              fieldlabel.parentNode.classList.remove('hidden')
              if (attrFor[attrFor.length-1] !== currentLang) {
                fieldlabel.parentNode.classList.add('hidden')
                translatedElement.classList.remove('hidden') // only re-reveal the parent class if we find this case.
              }
            })
          }
        } else {
          const translatedElement = labelList[label].parentElement;
          if (languageTag != null && languageTag != currentLang) {
            translatedElement.classList.add('hidden');
          } else {
            translatedElement.classList.remove('hidden');
          }
        }
      }
    }

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

  if (localStorage.selected_lang) {
    state.currentLang = localStorage.selected_lang;
    updateSelectedLanguage(state.currentLang);
    changeLanguage(state.currentLang);
    localStorage.removeItem('selected_lang');
  } else {
    state.currentLang = 'en';
    updateSelectedLanguage(state.currentLang);
    changeLanguage(state.currentLang);
  }

  // watch language select for changes
  $('#language-select').change(function(currentLang) {
    let selectedLanguage = document.getElementById('language-select')
      .selectedOptions[0];
    changeLanguage(selectedLanguage.id);
    updateSelectedLanguage(state.currentLang);
    localStorage.selected_lang = state.currentLang;
  });

  // case function for setting the selected language on dropdown
  // maybe there is a less verbose way to do this?
  function updateSelectedLanguage(currentLang) {
    var contentLink = document.getElementsByClassName('tab-nav merged')[0]
      .firstElementChild.firstElementChild;

    switch (currentLang) {
      case 'en':
        document.getElementById('language-select').value = 'English';
        contentLink.innerText = document.getElementById(
          'language-select',
        ).value;
        break;
      case 'es':
        document.getElementById('language-select').value = 'Spanish';
        contentLink.innerText = document.getElementById(
          'language-select',
        ).value;
        break;
      case 'vi':
        document.getElementById('language-select').value = 'Vietnamese';
        contentLink.innerText = document.getElementById(
          'language-select',
        ).value;
        break;
      case 'ar':
        document.getElementById('language-select').value = 'Arabic';
        contentLink.innerText = document.getElementById(
          'language-select',
        ).value;
        break;
    }
  }

  // Persist language for preview even after page refreshes on save
  var previewbutton = $('#page-preview-button');
  if (localStorage.preview_lang) {
    changeLanguage(localStorage.preview_lang);
    updateSelectedLanguage(localStorage.preview_lang);
    window.open(state.janisPreviewUrl, '_blank');
    localStorage.removeItem('preview_lang');
  }

  previewbutton.click(function() {
    let lang = null;
    if (localStorage.selected_lang) {
      lang = localStorage.selected_lang;
    }

    if (state.currentLang) {
      lang = state.currentLang;
    }

    localStorage.preview_lang = lang;
  });

  // Persist language for sharing even after page refreshes on save
  var shareButton = $('#page-share-preview-button');
  var urlcopied = $('#page-share-url-copied');
  shareButton.click(function() {
    // Not quite sure how the state/localstorage stuff is
    // working here but hopefully this gets us some links
    let lang = null;
    if (localStorage.selected_lang) {
      lang = localStorage.selected_lang;
    }

    if (state.currentLang) {
      lang = state.currentLang;
    }

    if (lang) {
      changeLanguage(lang);
      copyTextToClipboard(state.janisPreviewUrl);
      updateSelectedLanguage(lang);
      urlcopied.removeClass('hidden');
      urlcopied.fadeOut(10000);
      localStorage.sharingpreview = false;
    }
  });
  // Apply current language to new InlinePanels
  $('.add').click(function() {
    changeLanguage(state.currentLang);
    updateSelectedLanguage(state.currentLang);
  });

  var messages = $('.messages');
  messages.fadeOut(10000);

  // NOT sure the below is tracking anything
  // When we add new fields to the page (orderable/streamfields etc.)
  // only show the appropriate fields based on language
  // we can do this by observing changes to our sections count

  $('#sections-count').change(function() {
    changeLanguage(state.currentLang);
    updateSelectedLanguage(state.currentLang);
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

  // autocomplete for places
  (function() {
    var latlng = {
      lat: 30.26,
      lng: -97.73,
    };
    var placesAutocomplete = places({
      appId: 'plHX3G9C5GRN',
      apiKey: 'd9275f5f90784eb5ba59ff8ec581d9bb',
      container: document.querySelector('#id_physical_street'),
      templates: {
        value: function(suggestion) {
          return suggestion.name;
        },
      },
    }).configure({
      aroundLatLng: latlng.lat + ',' + latlng.lng,
      aroundRadius: 10 * 4000, // 40km radius
      type: 'address',
    });
    placesAutocomplete.on('change', function resultSelected(e) {
      document.querySelector('#id_physical_state').value =
        e.suggestion.administrative || '';
      document.querySelector('#id_physical_city').value =
        e.suggestion.city || '';
      document.querySelector('#id_physical_zip').value =
        e.suggestion.postcode || '';
      document.querySelector('#id_physical_country').value =
        e.suggestion.country || '';
    });
  })();
});
