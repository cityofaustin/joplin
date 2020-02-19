import ReactDOM from 'react-dom';
import React, { Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

import ChooseTypeStep from './ChooseTypeStep.js';
import ChooseTitleStep from './ChooseTitleStep.js';

import ButtonBar from './ButtonBar.js';

import './index.scss';

const MAX_TITLE_LENGTH = 58;
const DEPARTMENT_LIST = window.departments;

const stepsEnum = {
  CHOOSE_TYPE: 0,
  CHOOSE_TITLE: 1,
};

//TODO: extend this to support selecting a department
class CreateContentModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      type: null,
      title: '', // React warning said: `value` prop on `input` should not be null. Consider using an empty string...
      topic: null,
      theme: null,
      department: '',
      activeStep: 0,
      titleCharacterCount: 0,
      creatingContent: false,
      content_or_topic: 'content',
      missingTitle: false,
    };
  }

  onLastStep = () => {
    return this.state.activeStep === stepsEnum.CHOOSE_TITLE;
  };

  incrementActiveStep = () => {
    const nextStep = this.state.activeStep + 1;
    this.setState({ activeStep: nextStep });
  };

  decrementActiveStep = () => {
    let previousViableStep = this.state.activeStep - 1;

    // We can't go below zero
    if (previousViableStep < 0) {
      previousViableStep = stepsEnum.CHOOSE_TYPE;
    }

    this.setState({ activeStep: previousViableStep, missingTitle: false });
  };

  handleNextButton = e => {
    if (this.onLastStep()) {
      // Validate title max length
      if (this.state.titleCharacterCount > MAX_TITLE_LENGTH) return false;

      // Validate title min length
      if (this.state.titleCharacterCount <= 0) {
        this.setState({
          missingTitle: true,
        });
        return false;
      }

      this.setState(
        {
          creatingContent: true,
        },
        () => this.createPage(),
      );
      return;
    }

    this.incrementActiveStep();
  };

  handleBackButton = e => {
    this.decrementActiveStep();
  };

  handleTypeSelect = (dataObj, e) => {
    this.setState(
      {
        type: dataObj.type,
      },
      () => {
        this.incrementActiveStep();
      },
    );
  };

  handleContentOrTopicSelect = content_or_topic => {
    this.setState({ content_or_topic: content_or_topic });
  };

  handleTitleInputChange = e => {
    this.setState({
      title: e.target.value,
      titleCharacterCount: e.target.value.length,
      missingTitle: false,
    });
  };

  handleDepartmentSelect = e => {
    this.setState({ department: e.target.value });
  };

  redirectToEditPage = id => {
    window.location.href = `/admin/pages/${id}/edit/`;
  };

  createPage = () => {
    axios
      .post(
        '/admin/pages/new_from_modal/',
        {
          type: this.state.type,
          title: this.state.title,
          topic: this.state.topic,
          department: this.state.department,
          theme: this.state.theme,
        },
        { headers: { 'X-CSRFToken': Cookies.get('csrftoken') } },
      )
      .then(response => {
        // TODO: see if there's a better way to handle this
        window.onbeforeunload = null;

        this.redirectToEditPage(response.data.id);
      })
      .catch(error => {
        console.log(error);
      });
  };

  handleCloseButton = e => {
    this.setState({
      type: null,
      title: '', // React warning said: `value` prop on `input` should not be null. Consider using an empty string...
      topic: null,
      activeStep: 0,
      redirectUrl: null,
      titleCharacterCount: 0,
      missingTitle: false,
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
                {this.state.creatingContent ? (
                  <div className="CreateContentModal__step">
                    <h2 className="CreateContentModal__header">
                      Creating page
                    </h2>
                    <FontAwesomeIcon icon={faSpinner} spin size="5x" />
                  </div>
                ) : (
                  <div>
                    {this.state.activeStep === stepsEnum.CHOOSE_TYPE && (
                      <ChooseTypeStep
                        handleTypeSelect={this.handleTypeSelect}
                        handleContentOrTopicSelect={
                          this.handleContentOrTopicSelect
                        }
                        content_or_topic={this.state.content_or_topic}
                      />
                    )}
                    {this.state.activeStep === stepsEnum.CHOOSE_TITLE && (
                      <ChooseTitleStep
                        pageType={this.state.type}
                        title={this.state.title}
                        handleTitleInputChange={this.handleTitleInputChange}
                        characterCount={this.state.titleCharacterCount}
                        maxCharacterCount={MAX_TITLE_LENGTH}
                        departmentList={DEPARTMENT_LIST}
                        selectedDepartment={this.state.department}
                        handleDepartmentSelect={this.handleDepartmentSelect}
                      />
                    )}
                    {this.state.missingTitle && (
                      <p className="CreateContentModal__error">
                        Please enter a page title to continue.
                      </p>
                    )}
                    <ButtonBar
                      handleBackButton={this.handleBackButton}
                      handleNextButton={this.handleNextButton}
                      handleCloseButton={this.handleCloseButton}
                      hidden={this.state.activeStep === stepsEnum.CHOOSE_TYPE}
                      onLastStep={this.onLastStep()}
                    />
                  </div>
                )}
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
