import React from 'react';

import './ChooseTypeStep.scss';

import servicePageImage from '../../static/images/service_page_icon.svg';
import processPageImage from '../../static/images/process_page_icon.svg';

class ChooseTypeStep extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      content_or_topic: 'content',
    };
  }

  handleContentOrTopicSelect = (dataObj, e) => {
    this.setState({
      content_or_topic: dataObj.content_or_topic,
    });
  };

  render() {
    const { handleTypeSelect } = this.props;
    const content = this.state.content_or_topic === 'content';
    const topic = this.state.content_or_topic === 'topic';

    return (
      <div className="CreateContentModal__step">
        <div>
          <h2 className="CreateContentModal__header">Select a content type</h2>
          <div className="CreateContentModal__content_or_topic">
            {content ? (
              'Content pages'
            ) : (
              <a
                onClick={() =>
                  this.handleContentOrTopicSelect({
                    content_or_topic: 'content',
                  })
                }
              >
                Content pages
              </a>
            )}{' '}
            {topic ? (
              'Topic or topic collections'
            ) : (
              <a
                onClick={() =>
                  this.handleContentOrTopicSelect({ content_or_topic: 'topic' })
                }
              >
                Topic or topic collections
              </a>
            )}
          </div>
          <div className="ChooseTypeStep__options-wrapper">
            {content && (
              <React.Fragment>
                <div
                  className="ChooseTypeStep__option"
                  onClick={() =>
                    handleTypeSelect({
                      type: 'service',
                    })
                  }
                >
                  <img src={servicePageImage} alt="Service Page" />
                  <h3 className="ChooseTypeStep__option-header">
                    Service Page
                  </h3>
                  <p>A step by step guide to a particular city service.</p>
                </div>
                <div
                  className="ChooseTypeStep__option"
                  onClick={() =>
                    handleTypeSelect({
                      type: 'information',
                    })
                  }
                >
                  <h3 className="ChooseTypeStep__option-header">
                    Information Page
                  </h3>
                  <p>A page with information.</p>
                </div>
                <div
                  className="ChooseTypeStep__option"
                  onClick={() =>
                    handleTypeSelect({
                      type: 'department',
                    })
                  }
                >
                  <h3 className="ChooseTypeStep__option-header">
                    Department Page
                  </h3>
                  <p>Basic information and contact details for a department.</p>
                </div>
                <div
                  className="ChooseTypeStep__option"
                  onClick={() =>
                    handleTypeSelect({
                      type: 'official_document',
                    })
                  }
                >
                  <h3 className="ChooseTypeStep__option-header">
                    Official Document Page
                  </h3>
                  <p>A collection of official documents.</p>
                </div>
                <div
                  className="ChooseTypeStep__option"
                  onClick={() =>
                    handleTypeSelect({
                      type: 'guide',
                    })
                  }
                >
                  <h3 className="ChooseTypeStep__option-header">Guide Page</h3>
                  <p>A guide that references existing pages.</p>
                </div>
              </React.Fragment>
            )}
            {topic && (
              <React.Fragment>
                <div
                  className="ChooseTypeStep__option"
                  onClick={() =>
                    handleTypeSelect({
                      type: 'topic',
                    })
                  }
                >
                  <h3 className="ChooseTypeStep__option-header">Topic Page</h3>
                  <p>Basic information and links for a topic.</p>
                </div>
                <div
                  className="ChooseTypeStep__option"
                  onClick={() =>
                    handleTypeSelect({
                      type: 'topiccollection',
                    })
                  }
                >
                  <h3 className="ChooseTypeStep__option-header">
                    Topic Collection Page
                  </h3>
                  <p>A collection of topics.</p>
                </div>
              </React.Fragment>
            )}
          </div>
        </div>
      </div>
    );
  }
}

export default ChooseTypeStep;
