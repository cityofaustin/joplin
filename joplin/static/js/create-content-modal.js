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
      console.log('setup contentWizardModule...');
      this.registerEventHandlers();
    },
    registerEventHandlers: function() {
      var thiz = this;
      console.log(this);

      $('.js-page-select').click( function() {
        contentWizardState.type = $(this).data('contentType');
        contentWizardState.redirectUrl = $(this).data('redirecturl');
        thiz.incrementActiveStep();
        console.log(contentWizardState);
      });

      $('.js-select-topic').click(function(e) {
        contentWizardState.topic = $('.js-topic-item:checked[name=topic]').val();
        console.log(contentWizardState);
        thiz.writeToLocalStorage();
        debugger
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
    selectClickHandler: function(thing) {
    },
    incrementActiveStep: function(){
      contentWizardState.activeStep++;
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
    decrementActiveStep: function(){
      contentWizardState.activeStep--
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
    writeToLocalStorage: function() {
      localStorage.wagtailCreateModal = JSON.stringify(contentWizardState)
    }
  };

  contentWizardModule.init();
})
