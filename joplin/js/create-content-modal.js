import "../css/create_content_modal.scss";
import servicePageImage from '../static/images/service_page_icon.svg'
import processPageImage from '../static/images/process_page_icon.svg'

import React from "react";
import ReactDOM from "react-dom";

const CreateContentModal = () => {
  return (
    <div className="modal fade" id="createNewContentModal" tabIndex="-1" role="dialog" aria-labelledby="createNewContentModalLabel">
      <div className="js-create-content-wizard-form create-content-modal-wrapper">
        <div className="modal-dialog" role="document">
          <div className="modal-content create-content-modal">
            <div className="modal-body">
              <div className="js-wizard-step content-modal__step--active" data-active="true">
                <h2 className="content-modal__header">Select the Content Type</h2>
                <div className="content-modal__type-options-wrapper">
                  <div className="content-modal__type-option js-page-select"
                    data-content-type="service"
                    data-redirecturl="/admin/pages/add/base/servicepage/3/"
                  >
                    <img
                      src={servicePageImage}
                      alt="Service Page"
                    />
                    <h3 className="content-modal__type-option-header">Service Page</h3>
                    <p>A step by step guide to a particular city service.</p>
                  </div>
                  <div className="content-modal__type-option js-page-select"
                    data-content-type="process"
                    data-redirecturl="/admin/pages/add/base/processpage/3/"
                  >
                    <img
                      src={processPageImage}
                      alt="Service Page"
                    />
                    <h3 className="content-modal__type-option-header">Process Page</h3>
                    <p>Processes which require several steps, which may not go in order</p>
                  </div>
                  <div className="content-modal__type-option js-page-select"
                    data-content-type="department"
                    data-redirecturl="/admin/snippets/base/department/add/"
                  >
                    <h3 className="content-modal__type-option-header">Department Page</h3>
                    <p>Basic information and contact details for a department.</p>
                  </div>
                </div>
              </div>

              <div className="js-wizard-step content-modal__step--inactive" data-active="false">
                <h2 className="content-modal__header">
                  <span className="js-hideable-fields" data-show-for-department='false'>
                    Write an actionable title for your  <span className="js-page-type">service</span> page, starting with a verb.
                  </span>
                  <span className="js-hideable-fields content-modal__hidden" data-show-for-department='true'>
                    Write an the full name of the department, without abrreviations or acroynms.
                  </span>
                </h2>
                <label htmlFor="page-title" className="content-modal__input-label">
                  <span className="content-modal__input-label--left">Page Title</span>
                  <span className="content-modal__input-label--right">Character limit: 54</span>
                </label>
                <input type="text" id="page-title" autoFocus />
                <span className="content-modal__input-help js-hideable-fields" data-show-for-department='false'>
                  Example: Drop off hazardous wastes and other recyclables
                </span>

                <ul className="js-hideable-fields content-modal__input-bullet-list-help" data-show-for-department='false'>
                  <li>Use simple, accessible language</li>
                  <li>Use words you think residents may search to find the <span className="js-page-type">service</span></li>
                  <li>You don’t need to worry about including your department’s name in the title</li>
                </ul>
              </div>

              <div className="js-wizard-step content-modal__step--inactive" data-active="false">
                <h2>Select the topic  which best fits your content.</h2>

                {/* <!-- <div className="modal-button-row" style="display: block;">
                  <div className="button js-back">Back</div>
                  <button type="button" className="button" data-dismiss="modal">Close</button>
                  <div className="button js-continue js-select-topic" data-dismiss="modal">Continue</div>
                </div> --> */}
              </div>

              <div id="js-content-row" className="content-modal__button-row--hidden">
                <div className="content-modal__button js-back">Back</div>
                <button type="button" className="content-modal__button content-modal__button--reset" data-dismiss="modal">Close</button>
                <div className="content-modal__button js-continue">Continue</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(
  <CreateContentModal/>,
  document.getElementById("coa-create-content-modal")
);

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
