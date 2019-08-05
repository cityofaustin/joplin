import ReactDOM from 'react-dom';
import React, { Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

import ChooseTypeStep from './ChooseTypeStep.js';
import ChooseTopicOrDepartmentStep from './ChooseTopicOrDepartmentStep.js';
import ChooseTopicCollectionOrThemeStep from './ChooseTopicCollectionOrThemeStep.js';
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
  CHOOSE_TOPIC_COLLECTION_OR_THEME: 1,
  CHOOSE_DEPT_OR_TOPIC: 2,
  CHOOSE_DEPARTMENT: 3,
  CHOOSE_THEME: 4,
  CHOOSE_TITLE: 5,
};

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
    return this.state.activeStep === stepsEnum.CHOOSE_TITLE;
  };

  incrementActiveStep = () => {
    // If we're on the choose type step
    if (this.state.activeStep === stepsEnum.CHOOSE_TYPE) {
      // Department pages, topic pages, and service pages go straight to title
      if (
        this.state.type === 'department' ||
        this.state.type === 'service' ||
        this.state.type === 'topic'
      ) {
        this.setState({ activeStep: stepsEnum.CHOOSE_TITLE });
        return;
      }

      // Topic collection pages to to the select topic collection/theme step
      if (this.state.type === 'topiccollection') {
        this.setState({
          activeStep: stepsEnum.CHOOSE_TOPIC_COLLECTION_OR_THEME,
        });
        return;
      }

      // Process and information pages to to the select dept/topic step
      this.setState({ activeStep: stepsEnum.CHOOSE_DEPT_OR_TOPIC });
      return;
    }

    // If we're on choose department or choose theme, we need to go to choose title
    if (
      this.state.activeStep === stepsEnum.CHOOSE_DEPARTMENT ||
      this.state.activeStep === stepsEnum.CHOOSE_THEME
    ) {
      this.setState({ activeStep: stepsEnum.CHOOSE_TITLE });
      return;
    }
  };

  decrementActiveStep = () => {
    let previousViableStep = this.state.activeStep - 1;

    // We can't go below zero
    if (previousViableStep < 0) {
      previousViableStep = stepsEnum.CHOOSE_TYPE;
    }

    // we should only go to the theme select page if we have a theme
    if (previousViableStep === stepsEnum.CHOOSE_THEME && !this.state.theme) {
      previousViableStep--;
    }

    // Only topic collection pages can have a theme
    if (
      previousViableStep === stepsEnum.CHOOSE_THEME &&
      this.state.type !== 'topiccollection'
    ) {
      previousViableStep--;
    }

    // we should only go to the dept select page if we have a department
    if (
      previousViableStep === stepsEnum.CHOOSE_DEPARTMENT &&
      !this.state.department
    ) {
      previousViableStep--;
    }

    // We should never go back to the choose dept or topic page
    if (previousViableStep === stepsEnum.CHOOSE_DEPT_OR_TOPIC) {
      previousViableStep--;
    }

    // We should never go back to the choose topic collection or theme page
    if (previousViableStep === stepsEnum.CHOOSE_TOPIC_COLLECTION_OR_THEME) {
      previousViableStep--;
    }

    this.setState({ activeStep: previousViableStep });
  };

  handleNextButton = e => {
    if (this.onLastStep()) {
      // Validate title max length
      if (this.state.titleCharacterCount > MAX_TITLE_LENGTH) return false;

      // Validate title min length
      if (this.state.titleCharacterCount <= 0) return false;

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

  handleTopicOrDepartmentSelect = (dataObj, e) => {
    this.setState({
      activeStep:
        dataObj.topicOrDept === 'topic'
          ? stepsEnum.CHOOSE_TITLE
          : stepsEnum.CHOOSE_DEPARTMENT,
      department: null,
    });
  };

  handleTopicCollectionOrThemeSelect = (dataObj, e) => {
    this.setState({
      activeStep:
        dataObj.topicCollectionOrTheme === 'topiccollection'
          ? stepsEnum.CHOOSE_TITLE
          : stepsEnum.CHOOSE_THEME,
      theme: null,
    });
  };

  handleTitleInputChange = e => {
    this.setState({
      title: e.target.value,
      titleCharacterCount: e.target.value.length,
    });
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
          theme: this.state.theme,
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
                    {this.state.activeStep ===
                      stepsEnum.CHOOSE_DEPT_OR_TOPIC && (
                      <ChooseTopicOrDepartmentStep
                        handleTopicOrDepartmentSelect={
                          this.handleTopicOrDepartmentSelect
                        }
                      />
                    )}
                    {this.state.activeStep ===
                      stepsEnum.CHOOSE_TOPIC_COLLECTION_OR_THEME && (
                      <ChooseTopicCollectionOrThemeStep
                        handleTopicCollectionOrThemeSelect={
                          this.handleTopicCollectionOrThemeSelect
                        }
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
                      hidden={
                        this.state.activeStep === stepsEnum.CHOOSE_TYPE ||
                        this.state.activeStep ===
                          stepsEnum.CHOOSE_DEPT_OR_TOPIC ||
                        this.state.activeStep ===
                          stepsEnum.CHOOSE_TOPIC_COLLECTION_OR_THEME
                      }
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
