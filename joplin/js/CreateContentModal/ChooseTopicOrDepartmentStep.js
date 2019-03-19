import React from 'react';

import './ChooseTypeStep.scss';

const ChooseTopicOrDepartmentStep = ({ handleTopicOrDepartmentSelect }) => (
  <div className="CreateContentModal__step">
    <div>
      <h2 className="CreateContentModal__header">Topic or Department?</h2>
      <div className="ChooseTypeStep__options-wrapper">
        <div
          className="ChooseTypeStep__option"
          onClick={() =>
            handleTopicOrDepartmentSelect({
              type: 'topic',
            })
          }
        >
          <h3 className="ChooseTypeStep__option-header">Topic</h3>
          <p>This page will be a part of a topic.</p>
        </div>
        <div
          className="ChooseTypeStep__option"
          onClick={() =>
            handleTopicOrDepartmentSelect({
              type: 'department',
            })
          }
        >
          <h3 className="ChooseTypeStep__option-header">Department</h3>
          <p>This page applies exclusively to a specific department.</p>
        </div>
      </div>
    </div>
  </div>
);

export default ChooseTopicOrDepartmentStep;