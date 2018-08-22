import React, { Component } from 'react';
import plus from '../../static/images/plus.png';
import minus from '../../static/images/minus.png';
import unselected from '../../static/images/unselected.png';
import selected from '../../static/images/selected.png';

const TopicItem = ({ topic, handleTopicSelect, activeTopic }) => (
  <li
    onClick={handleTopicSelect.bind(this, topic.id)}
    className="ChooseTopicStep__topic-toggle"
  >
    <div
      className={
        activeTopic === topic.id
          ? "ChooseTopicStep__topic--selected"
          : "ChooseTopicStep__topic--unselected"
      }
    ></div>
    <span>{topic.text}</span>
  </li>
)

class ChooseTopicStep extends Component {
  constructor(props) {
    super(props);
    this.state = {
      openThemeGroup: 1,
    };
  }

  handleThemeToggle = (id, e) => {
    // This collapses the currently selected Theme Group when it is clicked
    if (Number(id) === this.state.openThemeGroup) {
      this.setState({
        openThemeGroup: 0,
      });
      return true;
    }
    this.setState({
      openThemeGroup: Number(id),
    });
  }

  render() {
    const themeTopicsTree = this.props.themeTopicTree;
    const arrayOfTopicsByTheme = Object.keys(themeTopicsTree);

    return (
      <div className="CreateContentModal__step">
        <h2>Select the topic  which best fits your content.</h2>
        <ul>
          {arrayOfTopicsByTheme.map((key) => {
            const themeGroup = themeTopicsTree[key];
            const isThemeGroupOpen = this.state.openThemeGroup === Number(key);

            return (
              <li key={`theme-${key}`} className="ChooseTopicStep__theme-group">
                <div onClick={this.handleThemeToggle.bind(this, key)} className="ChooseTopicStep__theme-toggle">
                  <div className={ isThemeGroupOpen ? 'ChooseTopicStep__minus' : 'ChooseTopicStep__plus' }></div>
                  <span className="ChooseTopicStep__topic-text">{themeGroup.text} Topics</span>
                </div>
                <ul className={ isThemeGroupOpen ? `ChooseTopicStep__theme-group--open` :  `ChooseTopicStep__theme-group--closed`}>
                  {themeGroup.topics.map(topic => (
                      <TopicItem
                        key={topic.id}
                        topic={topic}
                        activeTopic={this.props.topic}
                        handleTopicSelect={this.props.handleTopicSelect}
                      />
                    )
                  )}
                </ul>
              </li>
            );
          })}
        </ul>
      </div>
    );
  }
}

export default ChooseTopicStep;
