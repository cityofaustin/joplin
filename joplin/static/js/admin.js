document.addEventListener('DOMContentLoaded', function(event) {
  // HACK: I can't find a way to override this in python
  document.querySelector('label[for=id_title]').textContent = 'Actionable Title';

  // HACK: I can't find a way to configure this to be closed via python
  document.querySelectorAll('#extra_content-prependmenu:not(.stream-menu-closed)').forEach((elem) => {
    elem.click();
  });

  configureTranslationToggles();
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


function navigateWithHash() {
  let hash = window.location.hash.substr(1);
  if (hash) {
    let link = document.querySelector(`a[href='#${hash}']`);
    link && link.click();
  }
}


