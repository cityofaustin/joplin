import React, { Component } from 'react';
import plus from '../static/images/plus.png'
import minus from '../static/images/minus.png'
import unselected from '../static/images/unselected.png'
import selected from '../static/images/selected.png'
// import PropTypes from 'prop-types';

class ChooseTopicStep extends Component {
  constructor(props) {
    super(props);
    this.state = {
      openThemeGroup: 1,
    };
  }

  handleThemeToggle = (id, e) => {
    this.setState({
      openThemeGroup: Number(id)
    })
  }

  render() {
    const themeTopicsTree = this.props.themeTopicTree;
    const arrayOfTopicsByTheme = Object.keys(themeTopicsTree);

    return (
      <div className="content-modal__step">
        <h2>Select the topic  which best fits your content.</h2>
        <ul>
          {arrayOfTopicsByTheme.map((key) => {
            const themeGroup = themeTopicsTree[key]
            const isThemeGroupOpen = this.state.openThemeGroup === Number(key);
            return (
              <li key={`theme-${key}`}>
                <div onClick={this.handleThemeToggle.bind(this, key)}>
                  <img
                    src={ isThemeGroupOpen ? minus : plus }
                    alt={ isThemeGroupOpen ? 'close theme group' : 'open theme group' }
                  />
                </div>

                <span>{themeGroup.text} Topics</span>
                <ul className={ isThemeGroupOpen ? `ChooseTopicStep__theme-group--open` :  `ChooseTopicStep__theme-group--closed`}>
                  {themeGroup.topics.map(topic => {
                    return (
                      <li key={topic.id} onClick={this.props.handleTopicSelect.bind(this, topic.id)}>
                        <div>
                          { this.props.topic === topic.id
                              ? (
                                <img src={selected} alt=""/>
                              ) : (
                                <img src={unselected} alt=""/>
                              )
                          }
                          <span>{topic.text}</span>
                        </div>
                      </li>
                    )
                  })}
                </ul>
              </li>
            )
          })}
        </ul>
      </div>
    );
  }

}

// ChooseTopicStep.propTypes = {
//   : PropTypes.
// };

export default ChooseTopicStep;
