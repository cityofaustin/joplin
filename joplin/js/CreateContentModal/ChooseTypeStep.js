import React from 'react';

import './ChooseTypeStep.scss';

import servicePageImage from '../../static/images/service_page.png';
import infoPageImage from '../../static/images/info_page.png';
import departmentPageImage from '../../static/images/department_page.png';
import guideImage from '../../static/images/guide.png';
import documentsImage from '../../static/images/documents.png';
import topicCollectionImage from '../../static/images/topic_collection.png';
import topicsImage from '../../static/images/topics.png';
import formContainerImage from '../../static/images/info_page.png'; // TODO: get a png for forms from the xd
import locationImage from '../../static/images/location.png';

const PageTypeComponent = ({
  type,
  handleTypeSelect,
  name,
  image,
  description,
}) => (
  <div
    className="ChooseTypeStep__option"
    onClick={() => handleTypeSelect({ type })}
  >
    <h3 className="ChooseTypeStep__option-header">{name}</h3>
    <img src={image} alt={name} />
    <p>{description}</p>
  </div>
);

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
      description: 'A step by step guide to a particular city service.',
    },
    {
      type: 'information',
      name: 'Information Page',
      image: infoPageImage,
      description:
        'Provides supplementary information and resources to support service delivery.',
    },
    {
      type: 'department',
      name: 'Department Page',
      image: departmentPageImage,
      description: 'Basic information and contact details for a department.',
    },
    {
      type: 'guide',
      name: 'Guide',
      image: guideImage,
      description:
        'A collection of pages for a complicated process, organized into sections.',
    },
    {
      type: 'location',
      name: 'Location',
      image: locationImage,
      description:
        'Provides service, travel, and contact details for a location.',
    },
    {
      type: 'documents',
      name: 'Official document list',
      image: documentsImage,
      description: 'Summaries and links to official documents',
    },
    {
      type: 'form',
      name: 'Form container',
      image: formContainerImage,
      description: 'Container for an embedded Formstack form',
    },
    {
      type: 'event',
      name: 'Event details',
      image: formContainerImage,
      description: 'Details about an event',
    },
  ];

  const topicPages = [
    {
      type: 'topic',
      name: 'Topics',
      image: topicsImage,
      description:
        'Topics are landing pages that contain links to all pages on a particular subject',
    },
    {
      type: 'topiccollection',
      name: 'Topic Collection',
      image: topicCollectionImage,
      description:
        'Topic collections are landing pages that show similar topics within a larger subject',
    },
  ];

  return (
    <div className="CreateContentModal__step">
      <div>
        <h2 className="CreateContentModal__header">Select a content type</h2>
        <div className="CreateContentModal__content_or_topic">
          {/* whichever type is selected, show as text, otherwise a link to select*/}
          {content ? (
            'Content pages'
          ) : (
            <a onClick={() => handleContentOrTopicSelect('content')}>
              Content pages
            </a>
          )}
          <p className="CreateContentModal__content_or_topic--padding" />
          {topic ? (
            'Topic or topic collections'
          ) : (
            <a onClick={() => handleContentOrTopicSelect('topic')}>
              Topic or topic collections
            </a>
          )}
        </div>
        <div className="ChooseTypeStep__options-wrapper">
          {content && (
            <React.Fragment>
              {contentPages.map((contentPage, index) => (
                <PageTypeComponent
                  type={contentPage.type}
                  handleTypeSelect={handleTypeSelect}
                  name={contentPage.name}
                  image={contentPage.image}
                  description={contentPage.description}
                />
              ))}
            </React.Fragment>
          )}
          {topic && (
            <React.Fragment>
              {topicPages.map((topicPage, index) => (
                <PageTypeComponent
                  type={topicPage.type}
                  handleTypeSelect={handleTypeSelect}
                  name={topicPage.name}
                  image={topicPage.image}
                  description={topicPage.description}
                />
              ))}
            </React.Fragment>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChooseTypeStep;
