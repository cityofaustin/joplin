import React, { Component } from 'react';

import './ChooseTopicStep.scss';

import plus from '../../static/images/plus.png';
import minus from '../../static/images/minus.png';
import unselected from '../../static/images/unselected.png';
import selected from '../../static/images/selected.png';

const ThemeItem = ({ theme, handleThemeSelect, activeTheme }) => (
  <li
    onClick={handleThemeSelect.bind(this, theme.id)}
    className="ChooseTopicStep__topic-toggle"
  >
    <div
      className={`ChooseTopicStep__topic--${activeTheme === theme.id ? 'selected' : 'unselected'}`}
    ></div>
    <span>{theme.text}</span>
  </li>
)

class ChooseThemeStep extends Component {
  render() {
    const themeTopicsTree = this.props.themeTopicTree;

    return (
      <div className="CreateContentModal__step">
        <h2 className="CreateContentModal__header">
          Select the theme your topic belongs to.
        </h2>
        <ul>
          {Object.values(themeTopicsTree).map(theme => 
            <ThemeItem
              key={theme.id}
              theme={theme}
              activeTheme={this.props.theme}
              handleThemeSelect={this.props.handleThemeSelect}
            />
          )}
        </ul>
      </div>
    );
  }
}

export default ChooseThemeStep;
