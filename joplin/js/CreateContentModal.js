import ReactDOM from "react-dom";
import React, { Component } from 'react';

import ChooseTypeStep from './ChooseTypeStep.js'
import ChooseTitleStep from './ChooseTitleStep.js'
import ChooseTopicStep from './ChooseTopicStep.js'

import "../css/create_content_modal.scss";

const MAX_TITLE_LENGTH = 54;
const THEME_TOPIC_TREE = window.themeTopicsTree;

class CreateContentModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      type: null,
      title: '', // React warning said: `value` prop on `input` should not be null. Consider using an empty string...
      topic: null,
      activeStep: 0,
      redirectUrl: null,
      titleCharacterCount: 0,
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
    });
  }

  decrementActiveStep = () => {
    this.setState({
      activeStep: this.state.activeStep - 1
    });
  }

  handleNextButton = (e) => {
    // Validate title max length
    if (this.state.titleCharacterCount > MAX_TITLE_LENGTH) return false;

    // Skip Topic Select Step for creating a Department
    if (this.state.type === 'department' && this.state.activeStep === 1) {
      this.redirectToEditPage();
      return true;
    }

    this.incrementActiveStep();
  }

  handleBackButton = (e) => {
    this.decrementActiveStep();
  }

  handleTypeSelect = (dataObj, e) => {
    this.setState({
      type: dataObj.type,
      redirectUrl: dataObj.redirectUrl,
    });
    this.incrementActiveStep();
  }

  handleTitleInputChange = (e) => {
    this.setState({
      title: e.target.value,
      titleCharacterCount: e.target.value.length,
    });
  }

  handleTopicSelect = (e) => {
    this.setState({
      topic: e.target.value,
    });
    this.redirectToEditPage();
  }

  redirectToEditPage = () => {
    this.writeToLocalStorage();
    window.location.href = this.state.redirectUrl;
  }

  writeToLocalStorage = () => {
    localStorage.wagtailCreateModal = JSON.stringify(this.state);
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
                  <ChooseTitleStep
                    pageType={this.state.type}
                    title={this.state.title}
                    handleTitleInputChange={this.handleTitleInputChange}
                    characterCount={this.state.titleCharacterCount}
                    maxCharacterCount={MAX_TITLE_LENGTH}
                  />
                }
                { this.state.activeStep === 2 &&
                  <ChooseTopicStep
                    handleTopicSelect={this.handleTopicSelect}
                    themeTopicTree={THEME_TOPIC_TREE}
                  />
                }

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
