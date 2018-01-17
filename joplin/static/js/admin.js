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
  <div id="live-preview" class="preview-container hidden">
    <div class="thumbnail-container" title="Preview">
      <div class="thumbnail">
        <iframe src="" frameborder="0" onload="this.style.opacity = 1"></iframe>
      </div>
    </div>
  </div>
  `;
  document.body.insertAdjacentHTML('beforeend', previewHTMLString);

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

  const updateFn = _.debounce(updatePreviewViaSession, 800)
  editForm.addEventListener('input', updateFn);
  // This ensures we get updates for added snippets and other things the wagtail admin does that hides normal form flow
  editForm.addEventListener('DOMSubtreeModified', updateFn);
  updateFn();
}

function updatePreviewViaSession() {
  const form = document.querySelector('#page-edit-form');
  const button = form.querySelector('.action-preview');
  const previewURL = button.dataset.action;

  const baseOptions = {
    method: 'POST',
    credentials: 'same-origin',
  }

  const pageID = window.location.href.match(/pages\/(\d+)\/edit/).pop();
  const graphqlBody = `{
    pageData: servicePage(pk: ${pageID}, showPreview: true) {
      id
      title
      slug
      topic {
        id
        text
      }
      content
      extraContent
      contacts {
        edges {
          node {
            contact {
              name
              email
              phone
              hours {
                edges {
                  node {
                    dayOfWeek
                    startTime
                    endTime
                  }
                }
              }
              location {
                name
                street
                city
                state
                zip
                country
              }
            }
          }
        }
      }
    }
  }`;

  fetch(previewURL, Object.assign(baseOptions, {body: new FormData(form)}))
  .then((resp) => {
    const body = {
      query: graphqlBody,
    };
    const headers = {
      'Content-type': 'application/json',
    }
    return fetch('/api/graphql/', Object.assign(baseOptions, {body: JSON.stringify(body), headers: headers}));
  })
  .then((resp) => {
    return resp.json();
  })
  .then((json) => {
    const params = {
      preview: true,
      cache: Date.now(),
      d: JSON.stringify(json.data.pageData),
    };
    const qs = Object.keys(params).map(key => `${key}=${encodeURIComponent(params[key])}`).join('&');
    document.querySelector('#live-preview iframe').src = `${window.JANIS_URL}/service/68/?${qs}`;
  })
}


function navigateWithHash() {
  let hash = window.location.hash.substr(1);
  if (hash) {
    let link = document.querySelector(`a[href='#${hash}']`);
    link && link.click();
  }
}
