import React from 'react';
import classNames from 'classnames';

import './ButtonBar.scss';

const ButtonBar = ({
  hidden,
  handleBackButton,
  handleNextButton,
  handleCloseButton,
  onLastStep,
}) => (
  <div
    className={classNames({
      ButtonBar: !hidden,
      'ButtonBar--hidden': hidden,
    })}
  >
    <div className="ButtonBar__button" onClick={handleBackButton}>
      Back
    </div>
    <button
      type="button"
      className="ButtonBar__button ButtonBar__button--reset"
      data-dismiss="modal"
      onClick={handleCloseButton}
    >
      Close
    </button>
    <div className="ButtonBar__button" onClick={handleNextButton}>
      {onLastStep ? 'Create' : 'Continue'}
    </div>
  </div>
);

export default ButtonBar;
