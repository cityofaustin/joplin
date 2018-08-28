import React from 'react';

import './ChooseTitleStep.scss';

const ChooseTitleStep = ({
  pageType,
  title,
  handleTitleInputChange,
  characterCount,
  maxCharacterCount
}) => (
  <div className="CreateContentModal__step">
    <h2 className="CreateContentModal__header">
      { pageType === 'department' && (
        <span>
          Write an the full name of the department, without abrreviations or acroynms.
        </span>
      )}
      { pageType !== 'department' && (
        <span>
          Write an actionable title for your  {pageType} page, starting with a verb.
        </span>
      )}
    </h2>
    <label htmlFor="page-title" className="ChooseTitleStep__input-label">
      <span className="ChooseTitleStep__input-label--left">Page Title</span>
      { characterCount === 0
          ? (
            <span className="ChooseTitleStep__input-label--right">
              Character limit: 54
            </span>
          ) : (
            <span
              className={
                characterCount > maxCharacterCount
                  ? "ChooseTitleStep__input-label--right ChooseTitleStep__input-label--red"
                  : "ChooseTitleStep__input-label--right"
              }>
              Characters remaining: { maxCharacterCount - characterCount }
            </span>
          )
      }
    </label>
    <input
      value={title}
      type="text"
      id="page-title"
      autoFocus
      onChange={handleTitleInputChange}
    />

    { pageType !== 'department' && (
      <div>
        <span className="ChooseTitleStep__input-help">
          Example: Drop off hazardous wastes and other recyclables
        </span>
        <ul className="ChooseTitleStep__bullet-list">
          <li>Use simple, accessible language</li>
          <li>Use words you think residents may search to find the {pageType}</li>
          <li>You don’t need to worry about including your department’s name in the title</li>
        </ul>
      </div>
    )}
  </div>

);

export default ChooseTitleStep;
