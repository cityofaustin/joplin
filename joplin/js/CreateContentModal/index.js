import ReactDOM from 'react-dom';
import React, { Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

import ChooseTypeStep from './ChooseTypeStep.js';
import ChooseTopicOrDepartmentStep from './ChooseTopicOrDepartmentStep.js';
import ChooseTitleStep from './ChooseTitleStep.js';
import ChooseTopicStep from './ChooseTopicStep.js';
import ChooseThemeStep from './ChooseThemeStep.js';
import ChooseDepartmentStep from './ChooseDepartmentStep.js';
import ButtonBar from './ButtonBar.js';

import './index.scss';

const MAX_TITLE_LENGTH = 58;
const THEME_TOPIC_TREE = window.themeTopicsTree;
const DEPARTMENT_LIST = window.departments;

const stepsEnum = {
  CHOOSE_TYPE: 0,
  CHOOSE_TITLE: 1,
  CHOOSE_DEPT_OR_TOPIC: 2,
  CHOOSE_TOPIC: 3,
  CHOOSE_DEPARTMENT: 4,
  CHOOSE_THEME: 5,
}

class CreateContentModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      type: null,
      title: '', // React warning said: `value` prop on `input` should not be null. Consider using an empty string...
      topic: null,
      theme: null,
      department: null,
      activeStep: 0,
      titleCharacterCount: 0,
      creatingContent: false,
    };
  }

  onLastStep = () => {
    return (
      // If we're creating a department page, then the title step is the last step,
      // Otherwise, it'll be either the choose topic or choose department step
      (this.state.type === 'department' && this.state.activeStep === stepsEnum.CHOOSE_TITLE) ||
      this.state.activeStep === stepsEnum.CHOOSE_TOPIC || this.state.activeStep === stepsEnum.CHOOSE_DEPARTMENT || this.state.activeStep === stepsEnum.CHOOSE_THEME
    );
  };

  incrementActiveStep = () => {
    // If we're creating a service page and we're on the choose title page skip the
    // dept or topic selection because all service pages are topic only
    if(this.state.type === 'service' && this.state.activeStep === stepsEnum.CHOOSE_TITLE) {
      this.setState({
        activeStep: stepsEnum.CHOOSE_TOPIC
      });
      return;
    }

    // If we're creating a  page and we're on the choose title page skip to the
    // theme selection because all topic pages are theme only
    if(this.state.type === 'topic' && this.state.activeStep === stepsEnum.CHOOSE_TITLE) {
      this.setState({
        activeStep: stepsEnum.CHOOSE_THEME
      });
      return;
    }

    this.setState({
      activeStep: this.state.activeStep + 1,
    });
  };

  decrementActiveStep = () => {
    // If we're on choose topic or choose department or choose theme go back to page title page
    if(this.state.activeStep === stepsEnum.CHOOSE_TOPIC || this.state.activeStep === stepsEnum.CHOOSE_DEPARTMENT || this.state.activeStep === stepsEnum.CHOOSE_THEME) {
      this.setState({
        activeStep: stepsEnum.CHOOSE_TITLE
      });
      return;
    }

    this.setState({
      activeStep: this.state.activeStep - 1,
    });
  };

  handleNextButton = e => {
    // Validate title max length
    if (this.state.titleCharacterCount > MAX_TITLE_LENGTH) return false;

    // Validate title min length
    if (this.state.titleCharacterCount <= 0) return false;

    // If we're on the topic select step we need a topic selected
    if (this.state.activeStep === 2 && this.state.topic === null) return false;

    if (this.onLastStep()) {
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
    this.setState({
      type: dataObj.type,
    });
    this.incrementActiveStep();
  };

  handleTopicOrDepartmentSelect = (dataObj, e) => {
    this.setState({
      activeStep: dataObj.topicOrDept === 'topic' ? stepsEnum.CHOOSE_TOPIC : stepsEnum.CHOOSE_DEPARTMENT,
    });
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

  handleThemeSelect = id => {
    this.setState({ theme: id });
  };

  handleDepartmentSelect = id => {
    this.setState({ department: id });
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
          theme: this.state.theme
        },
        { headers: { 'X-CSRFToken': Cookies.get('csrftoken') } },
      )
      .then(response => {
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
                      Creating Page.
                    </h2>
                    <FontAwesomeIcon icon={faSpinner} spin size="5x" />
                  </div>
                ) : (
                  <div>
                    {this.state.activeStep === stepsEnum.CHOOSE_TYPE && (
                      <ChooseTypeStep
                        handleTypeSelect={this.handleTypeSelect}
                      />
                    )}
                    {this.state.activeStep === stepsEnum.CHOOSE_TITLE && (
                      <ChooseTitleStep
                        pageType={this.state.type}
                        title={this.state.title}
                        handleTitleInputChange={this.handleTitleInputChange}
                        characterCount={this.state.titleCharacterCount}
                        maxCharacterCount={MAX_TITLE_LENGTH}
                      />
                    )}
                    {this.state.activeStep === stepsEnum.CHOOSE_DEPT_OR_TOPIC && (
                      <ChooseTopicOrDepartmentStep
                        handleTopicOrDepartmentSelect={this.handleTopicOrDepartmentSelect}
                      />
                    )}
                    {this.state.activeStep === stepsEnum.CHOOSE_TOPIC && (
                      <ChooseTopicStep
                        topic={this.state.topic}
                        handleTopicSelect={this.handleTopicSelect}
                        themeTopicTree={THEME_TOPIC_TREE}
                      />
                    )}
                    {this.state.activeStep === stepsEnum.CHOOSE_DEPARTMENT && (
                      <ChooseDepartmentStep
                        department={this.state.department}
                        handleDepartmentSelect={this.handleDepartmentSelect}
                        departments={DEPARTMENT_LIST}
                      />
                    )}
                    {this.state.activeStep === stepsEnum.CHOOSE_THEME && (
                      <ChooseThemeStep
                        theme={this.state.theme}
                        handleThemeSelect={this.handleThemeSelect}
                        themeTopicTree={THEME_TOPIC_TREE}
                      />
                    )}
                    <ButtonBar
                      handleBackButton={this.handleBackButton}
                      handleNextButton={this.handleNextButton}
                      handleCloseButton={this.handleCloseButton}
                      hidden={this.state.activeStep === stepsEnum.CHOOSE_TYPE || this.state.activeStep === stepsEnum.CHOOSE_DEPT_OR_TOPIC}
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
