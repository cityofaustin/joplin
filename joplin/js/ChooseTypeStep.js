import React from 'react';
// import PropTypes from 'prop-types';

import servicePageImage from '../static/images/service_page_icon.svg'
import processPageImage from '../static/images/process_page_icon.svg'

const ChooseTypeStep = ({ handleTypeSelect }) => (
  <div>
    <div>
      <h2 className="content-modal__header">Select the Content Type</h2>
      <div className="content-modal__type-options-wrapper">
        <div className="content-modal__type-option"
          data-content-type="service"
          data-redirect-url="/admin/pages/add/base/servicepage/3/"
          onClick={handleTypeSelect}
        >
          <img
            src={servicePageImage}
            alt="Service Page"
          />
          <h3 className="content-modal__type-option-header">Service Page</h3>
          <p>A step by step guide to a particular city service.</p>
        </div>
        <div className="content-modal__type-option"
          data-content-type="process"
          data-redirect-url="/admin/pages/add/base/processpage/3/"
          onClick={handleTypeSelect}
        >
          <img
            src={processPageImage}
            alt="Service Page"
          />
          <h3 className="content-modal__type-option-header">Process Page</h3>
          <p>Processes which require several steps, which may not go in order</p>
        </div>
        <div className="content-modal__type-option"
          data-content-type="department"
          data-redirect-url="/admin/snippets/base/department/add/"
          onClick={handleTypeSelect}
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
