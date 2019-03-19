import React, { Component } from 'react';

import './ChooseTopicStep.scss';

import plus from '../../static/images/plus.png';
import minus from '../../static/images/minus.png';
import unselected from '../../static/images/unselected.png';
import selected from '../../static/images/selected.png';

const DepartmentItem = ({ department, handleDepartmentSelect, activeDepartment }) => (
  <li
    onClick={handleDepartmentSelect.bind(this, department.id)}
    className="ChooseTopicStep__topic-toggle"
  >
    <div
      className={`ChooseTopicStep__topic--${activeDepartment === department.id ? 'selected' : 'unselected'}`}
    ></div>
    <span>{department.title}</span>
  </li>
)

class ChooseDepartmentStep extends Component {
  render() {
    const { departments } = this.props;

    return (
      <div className="CreateContentModal__step">
        <h2 className="CreateContentModal__header">
          Select the department your content belongs to.
        </h2>
        <ul>
          {departments.map(department =>
            <DepartmentItem
              key={department.id}
              department={department}
              activeDepartment={this.props.department}
              handleDepartmentSelect={this.props.handleDepartmentSelect}
            />
          )}
        </ul>
      </div>
    );
  }
}

export default ChooseDepartmentStep;
