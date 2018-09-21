import ReactDOM from 'react-dom';
import React, { Component } from 'react';

import ChooseTypeStep from './ChooseTypeStep.js';
import ChooseTitleStep from './ChooseTitleStep.js';
import ChooseTopicStep from './ChooseTopicStep.js';
import ButtonBar from './ButtonBar.js';

import './index.scss';

const MAX_TITLE_LENGTH = 58;
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
    };
  }

  incrementActiveStep = () => {
    this.setState({
      activeStep: this.state.activeStep + 1,
    });
  };

  decrementActiveStep = () => {
    this.setState({
      activeStep: this.state.activeStep - 1,
    });
  };

  handleNextButton = e => {
    // Validate title max length
    if (this.state.titleCharacterCount > MAX_TITLE_LENGTH) return false;

    // Skip Topic Select Step for creating a Department
    if (this.state.type === 'department' && this.state.activeStep === 1) {
      this.redirectToEditPage();
      return;
    }

    if (this.state.activeStep === 2) {
      this.redirectToEditPage();
      return;
    }

    this.incrementActiveStep();
  };

  handleBackButton = e => {
    this.decrementActiveStep();
  };

  handleTypeSelect = (dataObj, e) => {
    this.setState({
      type: dataObj.type,
      redirectUrl: dataObj.redirectUrl,
    });
    this.incrementActiveStep();
  };

  handleTitleInputChange = e => {
    this.setState({
      title: e.target.value,
      titleCharacterCount: e.target.value.length,
    });
  };

  handleTopicSelect = id => {
    this.setState({ topic: id });
  };

  redirectToEditPage = () => {
    this.writeToLocalStorage();
    window.location.href = this.state.redirectUrl;
  };

  writeToLocalStorage = () => {
    localStorage.wagtailCreateModal = JSON.stringify(this.state);
  };

  handleCloseButton = e => {
    this.setState({
      type: null,
      title: '', // React warning said: `value` prop on `input` should not be null. Consider using an empty string...
      topic: null,
      activeStep: 0,
      redirectUrl: null,
      titleCharacterCount: 0,
    });
  };

  render() {
    return (
      <div
        className="modal fade"
        id="createNewContentModal"
        tabIndex="-1"
        role="dialog"
        aria-labelledby="createNewContentModalLabel"
      >
        <div className="CreateContentModal__wrapper">
          <div className="modal-dialog" role="document">
            <div className="modal-content CreateContentModal">
              <div className="modal-body">
                {this.state.activeStep === 0 && (
                  <ChooseTypeStep handleTypeSelect={this.handleTypeSelect} />
                )}
                {this.state.activeStep === 1 && (
                  <ChooseTitleStep
                    pageType={this.state.type}
                    title={this.state.title}
                    handleTitleInputChange={this.handleTitleInputChange}
                    characterCount={this.state.titleCharacterCount}
                    maxCharacterCount={MAX_TITLE_LENGTH}
                  />
                )}
                {this.state.activeStep === 2 && (
                  <ChooseTopicStep
                    topic={this.state.topic}
                    handleTopicSelect={this.handleTopicSelect}
                    themeTopicTree={THEME_TOPIC_TREE}
                  />
                )}
                <ButtonBar
                  handleBackButton={this.handleBackButton}
                  handleNextButton={this.handleNextButton}
                  handleCloseButton={this.handleCloseButton}
                  activeStep={this.state.activeStep}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <CreateContentModal />,
  document.getElementById('coa-CreateContentModal'),
);
