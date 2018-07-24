document.addEventListener("DOMContentLoaded", function(event) {
  // HACK: I can't find a way to override this in python
  const title = document.querySelector("label[for=id_title]");
  if (title) {
    debugger;
    title.textContent = "";
    titleLink = document.createElement("a");
    titleText = document.createTextNode("Actionable Title");
    titleLink.appendChild(titleText);
    titleLink.setAttribute(
      "href",
      "https://briaguya.github.io/digital-services-style-guide/writing-service-pages/#title"
    );
    titleLink.setAttribute("target", "sidebar-iframe");
    title.appendChild(titleLink);
  }

  // HACK: I can't find a way to configure this to be closed via python
  document
    .querySelectorAll("#extra_content-prependmenu:not(.stream-menu-closed)")
    .forEach(elem => {
      elem.click();
    });
});
