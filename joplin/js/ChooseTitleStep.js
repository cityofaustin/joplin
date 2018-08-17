import React from 'react';
// import PropTypes from 'prop-types';

const ChooseTitleStep = ({ pageType, title, handleTitleInputChange }) => (
  <div className="content-modal__step">
    <h2 className="content-modal__header">
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
    <label htmlFor="page-title" className="content-modal__input-label">
      <span className="content-modal__input-label--left">Page Title</span>
      <span className="content-modal__input-label--right">Character limit: 54</span>
    </label>
    <input
      value={title}
      type="text"
      id="page-title"
      autoFocus
      onChange={handleTitleInputChange}
    />

    { pageType !== 'department' && (
      <span className="content-modal__input-help">
        Example: Drop off hazardous wastes and other recyclables
      </span>
    )}

    { pageType !== 'department' && (
      <ul className="content-modal__input-bullet-list-help">
        <li>Use simple, accessible language</li>
        <li>Use words you think residents may search to find the <span className="js-page-type">service</span></li>
        <li>You don’t need to worry about including your department’s name in the title</li>
      </ul>
    )}
  </div>

);

// ChooseTitleStep.propTypes = {
//   : PropTypes.
// };

export default ChooseTitleStep;
