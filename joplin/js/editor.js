import '../css/editor.scss';
import '../css/preview.scss';

import menuActiveState from './EditPage/menuActiveState';
import toggleActivePanel from './SidebarPreview/toggleActivePanel';
import richTextPlaceholder from './EditPage/richTextPlaceholder';

import _ from 'lodash';

$(function() {
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

//  // TODO: what is this for??
// code from june 2018. (Because the current button placement doesn't allow me to put them inside the form to submit, I hooked up the new Publish & Save Draft buttons to just click the old buttons from hidden bottom bar. I also hooked up the Preview button to do what the old preview button does, but we'll want to change that to hook into the new preview flow once we've got that nailed down.)
//  $('.js-proxy-click').click(function() {
//    let $this = $(this);
//    $this.text($this.data('clicked-text'));
//
//    let $button;
//
//    let proxyByName = $this.data('proxyByName');
//    if (proxyByName) {
//      $button = $(`[name="${proxyByName}"]`);
//    }
//
//    let proxyByClass = $this.data('proxyByClass');
//    if (proxyByClass) {
//      $button = $(`.${proxyByClass}`);
//    }
//
//    if (!$button) {
//      console.error(`Data attributes: ${$this.data()}`);
//      throw new Error(
//        'Unable to find a button. Did you specify data-proxy-by-name or data-proxy-by-class?',
//      );
//    }
//
//    $button.click();
//  });

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
  // hides the translation fields by selecting the fields and adding the hidden tag
  function changeLanguage(currentLang) {
    state.currentLang = currentLang;
    setTabToContent();

    // replace brackets with hidden span tags and store lang tags in state
    function replaceLanguageLabels() {
      const languageLabels = $('ul[class="objects"]').find('label:contains(" [")');
      if (languageLabels.length) {
        // if state is undefined, set the language labels in state
        if (typeof state.languageLabels === 'undefined') {
          state.languageLabels = languageLabels;
        } else {
          console.log('its not undefined ', languageLabels.length)
          for (let label in languageLabels) {
            console.log(label, 'in lanaugage lables')
            state.languageLabels.push(languageLabels[label]);
          }
        }
        // replace brackets with hidden span tags
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
    let labelList = state.languageLabels;
    console.log(labelList.length, '  label list length')
    for (let label of labelList) {
      if (label.querySelector) {
        // language tag is either 'en', 'es', 'vi' or 'ar'
        let languageTag = label.querySelector('span').innerText;
        // these seem to be nested twice, from the title to the containing element
        // TODO: come up with a more elegant and maintainable way to check what elements ought to be hidden
        label.style.border = "1px solid #FF1493"
        label.parentElement.style.border = "3px solid green"
        if (
          label.parentElement.parentElement.parentElement.classList
            .value !== 'rah-static rah-static--height-auto c-sf-block__content'
        ) {
          const translatedElement = label.parentElement.parentElement;
          if (languageTag != null && languageTag != currentLang) {
            translatedElement.classList.add('hidden');
          } else {
            translatedElement.classList.remove('hidden');
          }
          /*  check if still valid with new react streamfield
              While the first condition checks for 'struct-blocks' with language tags,
              it doesn't catch the case where there are 'struct-blocks' with language
              tages WITHIN the element itself. The following condition checks for those conditions.
              - The was neccessary for guide stream fields. */
//          if (translatedElement.classList.contains('struct-block')) {
//            const fieldlabels = translatedElement.querySelectorAll('[for]');
//            fieldlabels.forEach(fieldlabel => {
//              const attrFor = fieldlabel.getAttribute('for').split('_');
//              fieldlabel.parentNode.classList.remove('hidden');
//              // Adding a failsafe to make sure we don't remove non translated fields
//              const attrLang = attrFor[attrFor.length - 1];
//              if (['en', 'es', 'vi', 'ar'].includes(attrLang)) {
//                if (attrLang !== currentLang) {
//                  fieldlabel.parentNode.classList.add('hidden');
//                  translatedElement.classList.remove('hidden'); // only re-reveal the parent class if we find this case.
//                }
//              }
//            });
//          }
        } else {
          const translatedElement = label.parentElement;
          if (languageTag != null && languageTag != currentLang) {
            translatedElement.classList.add('hidden');
          } else {
            translatedElement.classList.remove('hidden');
          }
        }
      } else {
        console.log(label, ' has no query selector')
      }
    }

    // ----
    // Switch the language for janisPreviewUrl in state
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

  // if we previously had a language stored in local storage, load the view for that language
  // otherwise, we default to english
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

  var structbutton = $('.c-sf-add-button'); // this only finds the first one, doesnt it?
  structbutton.click(function() {
      setTimeout(() => {
        const structlabels = $('label.field__label')
        for (const label of structlabels) {
          console.log(label.innerHTML)
          label.innerHTML = label.innerHTML.replace(
            '[',
            " <span style='display:none;'>");
          label.innerHTML = label.innerHTML.replace(']', '</span>');
        }
        console.log(structlabels.length)
      }, 100)
  })

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
    console.log('sections-count!!')
    changeLanguage(state.currentLang);
    updateSelectedLanguage(state.currentLang);
  });

  // do the same with locations on events
  $('#location_blocks-count').change(function() {
    console.log('locations count')
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
    console.log('sections count')
    trackChange(element);
  });

  // make sure observe all of them
  $('#location_blocks-count').each(function(index, element) {
    console.log('location blocks')
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
