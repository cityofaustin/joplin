export default function (){
  /* - MutationObserver for Wagtail JS handling
    - This function will handle flagged elements for custom styling and behavior.
    - Reference: https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver
      - Includes option to stop observing.
  */
  const wagtailFlaggedClassname = 'coa-option-description'
  const targetNode = document.getElementById('tab-content');

  const config = { attributes: true, childList: true, subtree: true };

  const callback = function(mutationsList) {

    for (let mutation of mutationsList) {
      if (mutation.type === 'childList') {
        let placeholder = mutation.target.querySelector('.public-DraftEditorPlaceholder-inner');
        if (placeholder) {
          let parent = placeholder;
          checkFlaggedAncestors(parent, placeholder);
        }
      }
    }

  }

  function checkFlaggedAncestors(parent, placeholder) {
    // - Here, we check up through all the element's direct parent nodes (ancestors),
    // - By only targeting the direct ancestors, we'll avoid other placeholders that we don't want to change.
    // - If a placeholder flag is present we add the class acordingly.
    //   - And, place our new placeholder text.
    while (parent = parent.parentNode) {
      if (
        parent.classList &&
        parent.classList.contains(wagtailFlaggedClassname)
      ) {
         placeholder.classList.add("coa-placeholder-elm")
         placeholder.innerText = "Option description"
        break;
      }
    }
  }

  // Create an observer instance linked to the callback function
  MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
  const observer = new MutationObserver(callback);

  // Start observing the target node for configured mutations
  observer.observe(targetNode, config);

}
