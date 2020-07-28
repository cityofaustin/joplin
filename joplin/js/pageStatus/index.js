require('../../joplin_UI/pageStatus.scss');

$(function() {
  // Open modal when user clicks on "Publishing" page_status badge
  $(".coa-page-status__open-modal-publishing").click(function(){
    $('#coa-page-status-modal__unpublishing').css("display", "none")
    $('#coa-page-status-modal__publishing').css("display", "block")
  })
  // Open modal when user clicks on "Unpublishing" page_status badge
  $(".coa-page-status__open-modal-unpublishing").click(function(){
    $('#coa-page-status-modal__publishing').css("display", "none")
    $('#coa-page-status-modal__unpublishing').css("display", "block")
  })

  // Close publishing modal when user clicks on X
  $("#coa-page-status-modal__publishing-close").click(function(){
    $('#coa-page-status-modal__publishing').css("display", "none")
  })
  // Close unpublishing modal when user clicks on X
  $("#coa-page-status-modal__unpublishing-close").click(function(){
    $('#coa-page-status-modal__unpublishing').css("display", "none")
  })

  // Close publishing message when user clicks on X
  $("#coa-message__publishing-close").click(function(){
    $('#coa-message__publishing').css("display", "none")
  })
  // Close unpublishing message when user clicks on X
  $("#coa-message__unpublishing-close").click(function(){
    $('#coa-message__unpublishing').css("display", "none")
  })
})
