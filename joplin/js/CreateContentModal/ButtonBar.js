import React from "react";
import classNames from "classnames";

import "./ButtonBar.scss";

const ButtonBar = ({
  activeStep,
  handleBackButton,
  handleNextButton,
  handleCloseButton
}) => (
  <div
    className={classNames({
      ButtonBar: activeStep > 0,
      "ButtonBar--hidden": activeStep === 0
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
      Continue
    </div>
  </div>
);

export default ButtonBar;
