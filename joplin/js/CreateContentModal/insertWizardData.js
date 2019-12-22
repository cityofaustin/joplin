export default function (){

    // Populate create new page fields when a user comes from the wizard
    if(localStorage.wagtailCreateModal) {
      const modalState = JSON.parse(localStorage.wagtailCreateModal);

      $("#id_topic").val(modalState.topic);
      if (modalState.type === "department") {
        $("#id_name").val(modalState.title);
      } else {
        $("#id_title").val(modalState.title);
      }
      localStorage.removeItem('wagtailCreateModal');
    }
};

// what is this?