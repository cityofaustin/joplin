import React from 'react';
// import PropTypes from 'prop-types';

import servicePageImage from '../static/images/service_page_icon.svg'
import processPageImage from '../static/images/process_page_icon.svg'

const ChooseTypeStep = ({ handleTypeSelect }) => (
  <div className="content-modal__step">
    <div>
      <h2 className="content-modal__header">Select the Content Type</h2>
      <div className="content-modal__type-options-wrapper">
        <div className="content-modal__type-option"
          onClick={handleTypeSelect.bind(this, {
            type: "service",
            // TODO: These redirectUrls could come from Python instead of being hard-coded
            redirectUrl: "/admin/pages/add/base/servicepage/3/",
          })}
        >
          <img
            src={servicePageImage}
            alt="Service Page"
          />
          <h3 className="content-modal__type-option-header">Service Page</h3>
          <p>A step by step guide to a particular city service.</p>
        </div>
        <div className="content-modal__type-option"
          onClick={handleTypeSelect.bind(this, {
            type: "process",
            redirectUrl: "/admin/pages/add/base/processpage/3/",
          })}
        >
          <img
            src={processPageImage}
            alt="Service Page"
          />
          <h3 className="content-modal__type-option-header">Process Page</h3>
          <p>Processes which require several steps, which may not go in order</p>
        </div>
        <div className="content-modal__type-option"
          onClick={handleTypeSelect.bind(this, {
            type: "department",
            redirectUrl: "/admin/snippets/base/department/add/",
          })}
        >
          <h3 className="content-modal__type-option-header">Department Page</h3>
          <p>Basic information and contact details for a department.</p>
        </div>
      </div>
    </div>

  </div>
);

// ChooseTypeStep.propTypes = {
//   blank: PropTypes.
// };

export default ChooseTypeStep;
