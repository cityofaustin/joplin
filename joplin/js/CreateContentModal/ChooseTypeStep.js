import React from 'react';

import './ChooseTypeStep.scss';

import servicePageImage from '../../static/images/service_page.png';
import infoPageImage from '../../static/images/info_page.png';
import departmentPageImage from '../../static/images/department_page.png';
import guideImage from '../../static/images/guide.png';
import documentsImage from '../../static/images/documents.png';
import topicCollectionImage from '../../static/images/topic_collection.png';
import topicsImage from '../../static/images/topics.png';
import formContainerImage from '../../static/images/info_page.png'; // TODO: get a png for forms

const ChooseTypeStep = ({
  handleTypeSelect,
  handleContentOrTopicSelect,
  content_or_topic,
}) => {
  const content = content_or_topic === 'content';
  const topic = content_or_topic === 'topic';

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
                handleContentOrTopicSelect({
                  content_or_topic: 'content',
                })
              }
            >
              Content pages
            </a>
          )}
          <p className="CreateContentModal__content_or_topic--padding" />
          {topic ? (
            'Topic or topic collections'
          ) : (
            <a
              onClick={() =>
                handleContentOrTopicSelect({ content_or_topic: 'topic' })
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
                <h3 className="ChooseTypeStep__option-header">Service Page</h3>
                <img src={servicePageImage} alt="Service Page" />
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
                <img src={infoPageImage} alt="Information Page" />
                <p>
                  Provides supplementary information and resources to support
                  service delivery
                </p>
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
                <img src={departmentPageImage} alt="Department Page" />
                <p>Basic information and contact details for a department.</p>
              </div>
              <div
                className="ChooseTypeStep__option"
                onClick={() =>
                  handleTypeSelect({
                    type: 'guide',
                  })
                }
              >
                <h3 className="ChooseTypeStep__option-header">Guide</h3>
                <img src={guideImage} alt="Guide" />
                <p>
                  A collection of pages for a complicated process, organized
                  into sections
                </p>
              </div>
              <div
                className="ChooseTypeStep__option"
                onClick={() =>
                  handleTypeSelect({
                    type: 'documents',
                  })
                }
              >
                <h3 className="ChooseTypeStep__option-header">
                  Official document list
                </h3>
                <img src={documentsImage} alt="Documents" />
                <p>Summaries and links to official documents</p>
              </div>
              <div
                className="ChooseTypeStep__option"
                onClick={() =>
                  handleTypeSelect({
                    type: 'form',
                  })
                }
              >
                <h3 className="ChooseTypeStep__option-header">
                  Form container
                </h3>
                <img src={formContainerImage} alt="form container" />
                <p>Container for an embedded Formstack form</p>
              </div>
            </React.Fragment>
          )}
          {topic && (
            <React.Fragment>
              <div
                className="ChooseTypeStep__option"
                onClick={() =>
                  handleTypeSelect({
                    type: 'topiccollection',
                  })
                }
              >
                <h3 className="ChooseTypeStep__option-header">
                  Topic Collection
                </h3>
                <img src={topicCollectionImage} alt="Topic Collection" />
                <p>
                  Topic collections are landing pages that show similar topics
                  within a larger subject
                </p>
              </div>
              <div
                className="ChooseTypeStep__option"
                onClick={() =>
                  handleTypeSelect({
                    type: 'topic',
                  })
                }
              >
                <h3 className="ChooseTypeStep__option-header">Topics</h3>
                <img src={topicsImage} alt="Topics" />
                <p>
                  Topics are landing pages that contain links to all pages on a
                  particular subject
                </p>
              </div>
            </React.Fragment>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChooseTypeStep;
