// TODO: This a better way
const anchors = {
  id_title: "#title",
  id_steps: "#steps",
  id_apps: "#apps",
  id_additional_content: "#additional",
  id_contacts: "#contacts",
  id_description: "#description",
  "id_process_steps-title": "#step-title",
  "id_process_steps-short_title": "#step-short-title",
  "id_process_steps-link_title": "#step-link-title",
  "id_process_steps-description": "#step-description",
  "id_process_steps-overview_steps": "#step-steps",
  "id_process_steps-detailed_content": "#step-details",
  "id_process_steps-quote": "#step-quote",
};

document.addEventListener("DOMContentLoaded", function(event) {
  // HACK: I can't find a way to override this in python
  // Get all labels and turn them into links
  const labels = document.querySelectorAll("label");
  const styleGuideUrl = document.getElementById("style_guide_url").value;

  for (const label of labels) {
    let id = label.getAttribute("for");

    // HACK: If we're dealing with subheadings in steps we need to remove the index
    if(id && id.includes("id_process_steps")) {
      const idTokens = id.split("-");
      id = `${idTokens[0]}-${idTokens[2]}`;
    }

    if (!id) {
      // HACK: Only some fields actually have for attributes
      switch (label.innerText) {
        case "ADD ANY MAPS OR APPS THAT WILL HELP THE RESIDENT USE THE SERVICE ":
          id = "id_apps";
          break;
        case "CONTACTS":
          id = "id_contacts";
          break;
        case "PROCESS STEPS":
          id = "id_steps";
          break;
      }
    }

    if (id in anchors) {
      text = document.createTextNode(label.textContent);
      label.textContent = "";
      if (id === "id_title") {
        text = document.createTextNode("Actionable Title");
      }
      link = document.createElement("a");
      link.appendChild(text);
      link.setAttribute("href", `${styleGuideUrl}/${anchors[id]}`);
      link.setAttribute("target", "sidebar-iframe");
      label.appendChild(link);
    }
  }

  // HACK: I can't find a way to configure this to be closed via python
  document
    .querySelectorAll("#extra_content-prependmenu:not(.stream-menu-closed)")
    .forEach(elem => {
      elem.click();
    });
});
