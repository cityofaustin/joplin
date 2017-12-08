document.addEventListener('DOMContentLoaded', function(event) {
  // HACK: I can't find a way to override this in python
  document.querySelector('label[for=id_title]').textContent = 'Actionable Title';

  // HACK: I can't find a way to configure this to be closed via python
  document.querySelectorAll('#extra_content-prependmenu:not(.stream-menu-closed)').forEach((elem) => {
    elem.click();
  });

  configureTranslationToggles();
  configureLivePreview();
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

function configureLivePreview() {
  if (!document.body.classList.contains('page-editor')) {
    return;
  }

  let previewHTMLString = `
  <div id="live-preview" class="preview-container">
    <div class="thumbnail-container" title="Preview">
      <div class="thumbnail">
        <iframe src="https://grackle.austintexas.io/" frameborder="0" onload="this.style.opacity = 1"></iframe>
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


function navigateWithHash() {
  let hash = window.location.hash.substr(1);
  if (hash) {
    let link = document.querySelector(`a[href='#${hash}']`);
    link && link.click();
  }
}


