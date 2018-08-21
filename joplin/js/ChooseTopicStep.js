import React, { Component } from 'react';
import plus from '../static/images/plus.png'
import minus from '../static/images/minus.png'
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
    console.log(this.state.openThemeGroup)
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
                <span>{themeGroup.text}</span>
                <ul className={ isThemeGroupOpen ? `ChooseTopicStep__theme-group--open` :  `ChooseTopicStep__theme-group--closed`}>
                  {themeGroup.topics.map(topic => {
                    return (
                      <li key={topic.id}>{topic.text}: id --- {topic.id}</li>
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
