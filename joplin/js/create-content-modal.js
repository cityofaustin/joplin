import ReactDOM from "react-dom";
import React, { Component } from 'react';

import ChooseTypeStep from './ChooseTypeStep.js'
import ChooseTitleStep from './ChooseTitleStep.js'
import ChooseTopicStep from './ChooseTopicStep.js'

import "../css/create_content_modal.scss";

class CreateContentModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      type: null,
      title: null,
      topic: null,
      activeStep: 0,
      redirectUrl: null,
    }
  }

  buttonRowClassName = () => {
    const baseclass = 'content-modal__button-row';

    if (this.state.activeStep > 0) {
      return baseclass;
    } else {
      return `${baseclass}--hidden`;
    }
  }

  incrementActiveStep = () => {
    this.setState({
      activeStep: this.state.activeStep + 1
    })
    // this.focusInput();
    // this.toggleActiveStep();
  }

  decrementActiveStep = () => {
    this.setState({
      activeStep: this.state.activeStep - 1
    })
    // this.focusInput();
    // this.toggleActiveStep();
  }

  handleNextButton = (e) => {
    this.incrementActiveStep();
  }

  handleBackButton = (e) => {
    this.decrementActiveStep();
  }

  handleTypeSelect = (e) => {
    this.setState({
      type: e.target.dataset.contentType,
      redirectUrl: e.target.dataset.redirectUrl,
    });
    this.incrementActiveStep();
  }


  render() {
    console.log(this.state)
    return (
      <div className="modal fade" id="createNewContentModal" tabIndex="-1" role="dialog" aria-labelledby="createNewContentModalLabel">
        <div className="js-create-content-wizard-form create-content-modal-wrapper">
          <div className="modal-dialog" role="document">
            <div className="modal-content create-content-modal">
              <div className="modal-body">
                { this.state.activeStep === 0 &&
                  <ChooseTypeStep handleTypeSelect={this.handleTypeSelect}/>
                }
                { this.state.activeStep === 1 &&
                  <ChooseTitleStep pageType={this.state.type}/>
                }
                { this.state.activeStep === 2 && <ChooseTopicStep/>}

                <div id="js-content-row" className={this.buttonRowClassName()}>
                  <div
                    className="content-modal__button"
                    onClick={this.handleBackButton}
                  >
                    Back
                  </div>
                  <button type="button" className="content-modal__button content-modal__button--reset" data-dismiss="modal">Close</button>
                  <div
                    className="content-modal__button"
                    onClick={this.handleNextButton}
                  >
                    Continue
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <CreateContentModal/>,
  document.getElementById("coa-create-content-modal")
);

$(document).ready(function() {

  // var contentWizardState = {
  //   type: '',
  //   title: '',
  //   topic: '',
  //   activeStep: 0,
  //   redirectUrl: '',
  // }

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
      //
      // $('.js-back').click( function(e) {
      //   e.preventDefault();
      //   console.log('js-back', contentWizardState);
      //   thiz.decrementActiveStep();
      // });
      //
      // $('.js-continue').click( function(e) {
      //   thiz.incrementActiveStep();
      // });
    },
    focusInput: function() {
      if (contentWizardState.activeStep === 1) {
        $('#page-title').get(0).focus();
      }
    },
    // toggleButtonRowVisibility: function () {
    //   if (contentWizardState.activeStep === 0) {
    //     $('#js-content-row').addClass('content-modal__button-row--hidden');
    //     $('#js-content-row').removeClass('content-modal__button-row');
    //   } else {
    //     $('#js-content-row').removeClass('content-modal__button-row--hidden');
    //     $('#js-content-row').addClass('content-modal__button-row');
    //   }
    // },
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
    // incrementActiveStep: function(){
    //   contentWizardState.activeStep++;
    //   this.toggleButtonRowVisibility();
    //   this.focusInput();
    //   this.toggleActiveStep();
    // },
    // decrementActiveStep: function(){
    //   contentWizardState.activeStep--;
    //   this.toggleButtonRowVisibility();
    //   this.focusInput();
    //   this.toggleActiveStep();
    // },
    writeToLocalStorage: function() {
      localStorage.wagtailCreateModal = JSON.stringify(contentWizardState)
    }
  };

  // contentWizardModule.init();
})
