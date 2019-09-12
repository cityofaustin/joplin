export default function (){
  /* - MutationObserver for Wagtail JS handling
    - This function will handle flagged elements for custom styling and behavior.
    - Reference: https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver
      - Includes option to stop observing.
  */
  const wagtailFlaggedClassname = 'odd-placeholder'
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

  function checkFlaggedAncestors(parent, placeholder){
    // - Here, we check up through all the elements direct parent nodes (ancestors),
    // - If a placeholder flag is present we add the class acordingly.
    while (parent = parent.parentNode) {
      if (
        parent.classList &&
        parent.classList.contains(wagtailFlaggedClassname)
      ) {
        parent.classList.forEach( classname => {
          const subClasses = classname.split('_');
          if (subClasses[0] === "odd-value") {
            placeholder.classList.add("odd-placeolder-elm")
            placeholder.innerText = subClasses[1].replace(/-/g," ");
          }
        })
      }
    }
  }

  // Create an observer instance linked to the callback function
  const observer = new MutationObserver(callback);

  // Start observing the target node for configured mutations
  observer.observe(targetNode, config);

}
