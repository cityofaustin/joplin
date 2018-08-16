$(document).ready(function() {

  var contentWizardState = {
    type: '',
    title: '',
    topic: '',
    activeStep: 0,
    redirectUrl: '',
  }

  var contentWizardModule = {
    init: function() {
      this.registerEventHandlers();
    },
    registerEventHandlers: function() {
      var thiz = this;

      $('.js-page-select').click( function() {
        contentWizardState.type = $(this).data('contentType');
        contentWizardState.redirectUrl = $(this).data('redirecturl');
        thiz.incrementActiveStep();
        $('.js-page-type').text($(this).data('contentType'));

        $('.js-hideable-fields').each( function (){

          // if department is active & field is show for department
          //   remove hidden
          // if department in not active  & field is show for department
          //   add hidden
          // if department is not active and field is not show for department
          //   remove hidden
          //
          console.log($(this))
          console.log('isDeptActive', contentWizardState.type === 'department')
          console.log('show-', $(this).data('showForDepartment') === "true")

          debugger

          if (contentWizardState.type === 'department' && $(this).data('showForDepartment') === 'true') {
            debugger
            $(this).removeClass('content-modal__hidden')
          } else if (contentWizardState.type === 'department') {
            $(this).addClass('content-modal__hidden')
          }
          // else if (contentWizardState.type !== 'department' && $(this).data('showForDepartment') === 'false') {
          //   $(this).addClass('content-modal__hidden')
          // } else if (contentWizardState.type !== 'department' && $(this).data('showForDepartment') === 'false') {
          //   $(this).removeClass('content-modal__hidden')
          // }
        })

        console.log(contentWizardState);
      });

      $('.js-select-topic').click(function(e) {
        contentWizardState.topic = $('.js-topic-item:checked[name=topic]').val();
        console.log(contentWizardState);
        thiz.writeToLocalStorage();
        window.location.href = contentWizardState.redirectUrl;
      });

      $('#page-title').keyup(function(e) {
        console.log('#page-title keyup', e.target.value)
        contentWizardState.title = e.target.value;
      });

      $('.js-back').click( function(e) {
        e.preventDefault();
        console.log('js-back', contentWizardState);
        thiz.decrementActiveStep();
      });

      $('.js-continue').click( function(e) {
        thiz.incrementActiveStep();
      });
    },
    focusInput: function() {
      if (contentWizardState.activeStep === 1) {
        $('#page-title').get(0).focus();
      }
    },
    toggleButtonRowVisibility: function () {
      if (contentWizardState.activeStep === 0) {
        $('#js-content-row').addClass('content-modal__button-row--hidden');
        $('#js-content-row').removeClass('content-modal__button-row');
      } else {
        $('#js-content-row').removeClass('content-modal__button-row--hidden');
        $('#js-content-row').addClass('content-modal__button-row');
      }
    },
    toggleActiveStep: function () {
      $('.js-wizard-step').each( function(i) {
        if (contentWizardState.activeStep === i) {
          $(this).addClass('content-modal__step--active');
          $(this).removeClass('content-modal__step--inactive');
        } else {
          $(this).removeClass('content-modal__step--active');
          $(this).addClass('content-modal__step--inactive');
        }
      });
    },
    incrementActiveStep: function(){
      contentWizardState.activeStep++;
      this.toggleButtonRowVisibility();
      this.focusInput();
      this.toggleActiveStep();
    },
    decrementActiveStep: function(){
      contentWizardState.activeStep--;
      this.toggleButtonRowVisibility();
      this.focusInput();
      this.toggleActiveStep();
    },
    writeToLocalStorage: function() {
      localStorage.wagtailCreateModal = JSON.stringify(contentWizardState)
    }
  };

  contentWizardModule.init();
})
