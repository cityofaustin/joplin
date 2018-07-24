// TODO: This a better way
const anchorLinks = {
  id_title:
    "https://briaguya.github.io/digital-services-style-guide/writing-service-pages/#title",
  id_steps:
    "https://briaguya.github.io/digital-services-style-guide/writing-service-pages/#steps",
  id_apps:
    "https://briaguya.github.io/digital-services-style-guide/writing-service-pages/#apps",
  id_additional_content:
    "https://briaguya.github.io/digital-services-style-guide/writing-service-pages/#additional",
  "id_contacts-0-contact":
    "https://briaguya.github.io/digital-services-style-guide/writing-service-pages/#contacts"
};

document.addEventListener("DOMContentLoaded", function(event) {
  // HACK: I can't find a way to override this in python
  // Get all labels and turn them into links
  const labels = document.querySelectorAll("label");
  for (const label of labels) {
    const id = label.getAttribute("for");
    console.log(id);
  }
  debugger;
  for (const label of labels) {
    const id = label.getAttribute("for");
    if (id in anchorLinks) {
      text = document.createTextNode(label.textContent);
      label.textContent = "";
      if (id === "id_title") {
        text = document.createTextNode("Actionable Title");
      }
      link = document.createElement("a");
      link.appendChild(text);
      link.setAttribute("href", anchorLinks[id]);
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
