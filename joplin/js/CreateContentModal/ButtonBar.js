import React from 'react';

const buttonRowClassName = (activeStep) => {
  const baseclass = 'ButtonBar';

  if (activeStep > 0) {
    return baseclass;
  } else {
    return `${baseclass}--hidden`;
  }
}

const ButtonBar = ({ activeStep, handleBackButton, handleNextButton }) => (
  <div className={buttonRowClassName(activeStep)}>
    <div
      className="ButtonBar__button"
      onClick={handleBackButton}
    >
      Back
    </div>
    <button type="button"
      className="ButtonBar__button ButtonBar__button--reset"
      data-dismiss="modal"
    >
      Close
    </button>
    <div
      className="ButtonBar__button"
      onClick={handleNextButton}
    >
      Continue
    </div>
  </div>
);

export default ButtonBar;
