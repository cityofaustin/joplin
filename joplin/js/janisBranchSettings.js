// If "URL" is selected, then only show input field for preview_janis_url
// Else, "Branch Name" is selected and we should show field for preview_janis_branch
const togglePreviewSettings = previewInputValue => {
  if (previewInputValue === 'url') {
    $('.preview_janis_url-container').show();
    $('.preview_janis_branch-container').hide();
  } else {
    $('.preview_janis_url-container').hide();
    $('.preview_janis_branch-container').show();
  }
};

$(function() {
  // Only run code when editing janisbranchsettings
  if (location.pathname === '/admin/settings/base/janisbranchsettings/1/') {
    const previewInputNode = $('select#id_preview_input');
    togglePreviewSettings(previewInputNode.val());
    previewInputNode.change(function() {
      togglePreviewSettings($(this).val());
    });
  }
});
