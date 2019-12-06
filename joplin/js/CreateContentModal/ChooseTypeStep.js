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
import locationImage from '../../static/images/location.png';

const ChooseTypeStep = ({
  handleTypeSelect,
  handleContentOrTopicSelect,
  content_or_topic,
}) => {
  const content = content_or_topic === 'content';
  const topic = content_or_topic === 'topic';

  const contentPages = [
    {
      type: 'service',
      name: 'Service Page',
      image: servicePageImage,
      description: 'A step by step guide to a particular city service.'
    },
    {
      type: 'information',
      name: 'Information Page',
      image: infoPageImage,
      description: 'Provides supplementary information and resources to support service delivery.'
    },
    {
      type: 'department',
      name: 'Department Page',
      image: departmentPageImage,
      description: 'Basic information and contact details for a department.'
    },
    {
      type: 'guide',
      name: 'Guide',
      image: guideImage,
      description: 'A collection of pages for a complicated process, organized into sections.'
    },
    {
      type: 'location',
      name: 'Location',
      image: locationImage,
      description: 'Provides service, travel, and contact details for a location.'
    },
    {
      type: 'documents',
      name: 'Official document list',
      image: documentsImage,
      description: 'Summaries and links to official documents'
    },
    {
      type: 'form',
      name: 'Form container',
      image: formContainerImage,
      description: 'Container for an embedded Formstack form'
    }
  ];

  const topicPages = [
    {
      type: 'topic',
      name: 'Topics',
      image: topicsImage,
      description: 'Topics are landing pages that contain links to all pages on a particular subject'
    },
    {
      type: 'topiccollection',
      name: 'Topic Collection',
      image: topicCollectionImage,
      description: 'Topic collections are landing pages that show similar topics within a larger subject'
    }
  ]
  console.log(content_or_topic);

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
              {contentPages.map((contentPage, index) => (
                <div
                className="ChooseTypeStep__option"
                onClick={() =>
                  handleTypeSelect({
                    type: contentPage.type,
                  })
                }
              >
                <h3 className="ChooseTypeStep__option-header">{contentPage.name}</h3>
                <img src={contentPage.image} alt={contentPage.name} />
                <p>{contentPage.description}</p>
              </div>
            ))}
            </React.Fragment>
          )}
          {topic && (
            <React.Fragment>
              {topicPages.map((topicPage, index) => (
              <div
                className="ChooseTypeStep__option"
                onClick={() =>
                  handleTypeSelect({
                    type: topicPage.type,
                  })
                }
              >
                <h3 className="ChooseTypeStep__option-header">
                  {topicPage.name}
                </h3>
                <img src={topicPage.image} alt={topicPage.name} />
                <p>
                  {topicPage.description}
                </p>
              </div>))}
            </React.Fragment>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChooseTypeStep;
