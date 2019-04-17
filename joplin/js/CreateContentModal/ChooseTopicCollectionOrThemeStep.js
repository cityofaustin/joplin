import React from 'react';

import './ChooseTypeStep.scss';

const ChooseTopicCollectionOrThemeStep = ({ handleTopicCollectionOrThemeSelect }) => (
  <div className="CreateContentModal__step">
    <div>
      <h2 className="CreateContentModal__header">Topic Collection or Theme?</h2>
      <div className="ChooseTypeStep__options-wrapper">
        <div
          className="ChooseTypeStep__option"
          onClick={() =>
            handleTopicCollectionOrThemeSelect({
              topicCollectionOrTheme: 'topiccollection',
            })
          }
        >
          <h3 className="ChooseTypeStep__option-header">Topic Collection</h3>
          <p>This page will be a part of another topic collection.</p>
        </div>
        <div
          className="ChooseTypeStep__option"
          onClick={() =>
            handleTopicCollectionOrThemeSelect({
              topicCollectionOrTheme: 'theme',
            })
          }
        >
          <h3 className="ChooseTypeStep__option-header">Theme</h3>
          <p>This page will be a part of a theme.</p>
        </div>
      </div>
    </div>
  </div>
);

export default ChooseTopicCollectionOrThemeStep;