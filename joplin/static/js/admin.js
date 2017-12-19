document.addEventListener('DOMContentLoaded', function(event) {
  // HACK: I can't find a way to override this in python
  const title = document.querySelector('label[for=id_title]');
  if (title) {
    title.textContent = 'Actionable Title';
  }

  // HACK: I can't find a way to configure this to be closed via python
  document.querySelectorAll('#extra_content-prependmenu:not(.stream-menu-closed)').forEach((elem) => {
    elem.click();
  });

  configureTranslationToggles();
  configurePreviewWindow();
  configurePreviewUpdates();
  navigateWithHash();
});

function configureTranslationToggles() {
  // Add toggle button
  document.querySelectorAll('.translation-tab .object h2').forEach((elem) => {
    let elemID = 9;
    let toggleHTMLString = `
    <div class="toggle" style="float: right;">
      <div>Show Original</div>
      <input class="tgl tgl-flat" id="${elemID}" type="checkbox" checked>
      <label class="tgl-btn" for="${elemID}"></label>
    </div>
    `;

    elem.insertAdjacentHTML('beforeend', toggleHTMLString)
  });

  // Listen for toggle button
  document.addEventListener('change', (ev) => {
    if (!ev.target.classList.contains('tgl')) {
      return;
    }

    const parentElem = ev.target.closest('.object');
    const helpElemClassList = parentElem.querySelector('.object-help').classList;
    helpElemClassList.toggle('hidden');
    // This is gross because wagtail uses absolute position containers so we need to move
    // the field around based on what's on top of it
    parentElem.querySelector('fieldset').style['padding-top'] = helpElemClassList.contains('hidden') ? '4em' : '0.5em';
  });
}

function configurePreviewWindow() {
  if (!document.body.classList.contains('page-editor')) {
    return;
  }

  let pageID = window.location.href.split('/').find((item) => item && !isNaN(item));
  let previewHTMLString = `
  <div id="live-preview" class="preview-container">
    <div class="thumbnail-container" title="Preview">
      <div class="thumbnail">
        <iframe src="${window.JANIS_URL}/service/${pageID}" frameborder="0" onload="this.style.opacity = 1" sandbox="allow-scripts"></iframe>
      </div>
    </div>
  </div>
  `;
  let el = document.body.insertAdjacentHTML('beforeend', previewHTMLString);

  document.addEventListener('click', (ev) => {
    if (!ev.target.classList.contains('action-preview')) {
      return;
    }

    ev.preventDefault();
    ev.stopPropagation();

    document.querySelector('#live-preview').classList.toggle('hidden');
  }, true);
}

function configurePreviewUpdates() {
  const editForm = document.querySelector('form#page-edit-form');
  if (!editForm) {
    return;
  }

  editForm.addEventListener('input', _.debounce(updatePreviewWindow, 800));
}

function updatePreviewWindow() {
  let controls = document.querySelector('form#page-edit-form').elements;
  let d = {};
  for(let i = 0; i < controls.length; i++) {
    let el = controls[i];
    let elType = el.type;
    if (!el.name || el.hidden || elType === 'submit' || el.name.endsWith('-count')) {
      continue;
    }

    let path = el.name.split('-').reduce((accumulatedVal, key) => {
      return accumulatedVal + (Number.isNaN(Number.parseInt(key)) ? `.${key}` : `[${key}]`)
    });
    console.debug(`${elType} ${el.name} = ${el.value} (path = ${path})`);

    if (elType === 'select') {
      _.set(d, path, {
        id: el.value,
        text: encodeURIComponent(el.options[el.selectedIndex].text),
      })
    }
    else if (['text', 'textarea', 'input', 'hidden'].includes(elType)) {
      _.set(d, path, encodeURIComponent(el.value));
    }
  }

  console.log('Preview data', d);

  let params = {
    preview: true,
    cache: Date.now(),
    d: JSON.stringify(d),
  };
  let qs = Object.keys(params).map(key => `${key}=${params[key]}`).join('&');

  document.querySelector('#live-preview iframe').src = `${window.JANIS_URL}/service/68?${qs}`;
}


function navigateWithHash() {
  let hash = window.location.hash.substr(1);
  if (hash) {
    let link = document.querySelector(`a[href='#${hash}']`);
    link && link.click();
  }
}


