import React from 'react';
import classNames from 'classnames';

import './ChooseTitleStep.scss';

const getPageHeading = (pageType) => {
  switch(pageType) {
    case 'service':
      return 'Write an actionable title for your service page, starting with a verb.';
    case 'information':
      return 'Write a clear, descriptive title.'
    case 'department': 
      return 'Write the full name of the department without abbreviations or acronyms.';
    case 'guide':
      return 'Write a name for your guide.';
    case 'documents':
      return 'Write the name for this list of documents';
    case 'form': 
      return 'Write the name for this form';
    case 'location':
      return 'Write the name of this location.';
    default: 
      return '';
  }
}

const ChooseTitleStep = ({
  pageType,
  title,
  handleTitleInputChange,
  characterCount,
  maxCharacterCount,
}) => (
  <div className="CreateContentModal__step">
    <h2 className="CreateContentModal__header">
      <span>{getPageHeading(pageType)}</span>
    </h2>
    <label htmlFor="page-title" className="ChooseTitleStep__input-label">
      <span className="ChooseTitleStep__input-label--left">
        {pageType === 'location' ? 'Location name' : 'Page Title'}</span>
      <span
        className={classNames('ChooseTitleStep__input-label--right', {
          'ChooseTitleStep__input-label--red':
            characterCount > maxCharacterCount,
        })}
      >
        Characters remaining: {maxCharacterCount - characterCount}
      </span>
    </label>
    <input
      value={title}
      type="text"
      id="page-title"
      autoFocus
      onChange={handleTitleInputChange}
    />

    {pageType === 'department' ? (
      <div>
        <span className="ChooseTitleStep__input-help">
          Example: Public Health
        </span>
        <ul className="ChooseTitleStep__bullet-list">
          <li>You don't need to include "Austin" in your department name.</li>
        </ul>
      </div>
    )
    : (
      <div>
        <span className="ChooseTitleStep__input-help">
          {pageType === 'service' &&
            'Example: Drop off hazardous wastes and other recyclables'}
          {pageType === 'guide' &&
            'Example: Guide for starting a community garden'}
          {pageType === 'information' && 'Example: Hepatitis in Austin'}
        </span>

        <ul className="ChooseTitleStep__bullet-list">
          {pageType === 'guide' && <li>Use the word "guide" in your title.</li>}
          {pageType === 'information' && <li>Use primary and secondary keywords.</li>}
          <li>Use simple, accessible language.</li>
          <li>
            Use words you think residents may search to find the {pageType}.
          </li>
          <li>
            You don’t need to include your department’s name in the title.
          </li>
        </ul>
      </div>
    )}
  </div>
);

export default ChooseTitleStep;
