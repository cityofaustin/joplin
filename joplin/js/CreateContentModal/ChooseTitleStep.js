import React from 'react';
import classNames from 'classnames';

import './ChooseTitleStep.scss';

const getPageHeading = pageType => {
  switch (pageType) {
    case 'service':
      return 'Write an actionable title for your service page, starting with a verb.';
    case 'information':
      return 'Write a clear, descriptive title.';
    case 'department':
      return 'Write the full name of the department without abbreviations or acronyms.';
    case 'guide':
      return 'Write a name for your guide.';
    case 'documents':
      return 'Write the name for this document';
    case 'documentscollection':
      return 'Write the name for this list of documents';
    case 'form':
      return 'Write the name for this form';
    case 'location':
      return 'Write the name of this location.';
    case 'event':
      return 'Write the name of this event.';
    case 'importSinglePage':
      return 'Paste a preview URL for the page you want to import';
    default:
      return '';
  }
};

const getInputLabel = pageType => {
  switch (pageType) {
    case 'location':
      return 'Location name';
    case 'event':
      return 'Event name';
    case 'importSinglePage':
      return 'URL';
    case 'documentscollection':
      return 'List Title';
    case 'documents':
      return 'Document Title'
    default:
      return 'Page Title';
  }
};

const ChooseTitleStep = ({
  pageType,
  title,
  handleTitleInputChange,
  jwtToken,
  handleJwtTokenInputChange,
  characterCount,
  maxCharacterCount,
  departmentList,
  selectedDepartment,
  handleDepartmentSelect
}) => (
  <div className="CreateContentModal__step">
    <h2 className="CreateContentModal__header">
      <span>{getPageHeading(pageType)}</span>
    </h2>
    <label htmlFor="page-title" className="ChooseTitleStep__input-label">
      <span className="ChooseTitleStep__input-label--left">
        {getInputLabel(pageType)}
      </span>
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
    {
      (pageType === 'importSinglePage') &&
      (
        <React.Fragment>
          <label htmlFor="page-title" className="ChooseTitleStep__input-label">
            <span className="ChooseTitleStep__input-label--left">
              JWT Token
            </span>
          </label>
          <input
            value={jwtToken}
            type="text"
            id="jwt-token"
            autoFocus
            onChange={handleJwtTokenInputChange}
          />
        </React.Fragment>
      )
    }
    { // We don't get sent a list of departments unless the user is an admin
      // so if we have one, we should show the dropdown
      !!departmentList && !!departmentList.length &&
    <label htmlFor="page-department" className="ChooseTitleStep__input-label">
      Pick a department
      <select id="page-department" value={selectedDepartment} onChange={handleDepartmentSelect}>
        <option value=''></option>
        {departmentList.map(dept => <option value={dept.id}>{dept.title}</option>)}
      </select>
    </label>}

    {(pageType === 'department') && (
      <div>
        <span className="ChooseTitleStep__input-help">
          Example: Public Health
        </span>
        <ul className="ChooseTitleStep__bullet-list">
          <li>You don't need to include "Austin" in your department name.</li>
        </ul>
      </div>
    )}
    {(pageType === 'importSinglePage') && (
      <ul className="ChooseTitleStep__bullet-list">
        <li>Add a Preview URL with the revision that you want to import.</li>
        <li>For now, only accepts imports from 'janis.austintexas.io' and 'janis-pytest.netlify.com'</li>
        <li>You must provide your own JWT token for the site you're importing from.</li>
        <li>Check documentation to learn how to get a JWT token.</li>
      </ul>
    )}
    {((pageType !== 'department') && (pageType !== 'importSinglePage')) && (
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
          {pageType === 'information' && (
            <li>Use primary and secondary keywords.</li>
          )}
          <li>Use simple, accessible language.</li>
          <li>
            Use words you think residents may search to find the {pageType}.
          </li>
          <li>
            {pageType === 'event'
              ? `You don’t need to worry about including the location or your department’s name in the title.`
              : `You don’t need to include your department’s name in the title.`}
          </li>
        </ul>
      </div>
    )}
  </div>
);

export default ChooseTitleStep;
