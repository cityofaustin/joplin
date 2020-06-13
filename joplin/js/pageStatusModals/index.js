require('../../joplin_UI/pageStatus.scss');

$(function() {
  // Open modal when user clicks on "Publishing" page_status badge
  $(".coa-page-status__open-modal.coa-page-status__publishing-badge").click(function(){
    $('#coa-page-status-modal__unpublishing').css("display", "none")
    $('#coa-page-status-modal__publishing').css("display", "block")
    console.log("hello pub")
  })
  // Open modal when user clicks on "Unpublishing" page_status badge
  $(".coa-page-status__open-modal.coa-page-status__unpublishing-badge").click(function(){
    $('#coa-page-status-modal__publishing').css("display", "none")
    $('#coa-page-status-modal__unpublishing').css("display", "block")
    console.log("hello unpub")
  })

  // Close publishing modal when user clicks on X
  $("#coa-page-status-modal__publishing-close").click(function(){
    $('#coa-page-status-modal__publishing').css("display", "none")
    console.log("Goodbye pub")
  })
  // Close unpublishing modal when user clicks on X
  $("#coa-page-status-modal__unpublishing-close").click(function(){
    $('#coa-page-status-modal__unpublishing').css("display", "none")
    console.log("Goodbye unpub")
  })
})
