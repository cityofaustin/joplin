from gql import gql

queries = {
    'topiccollection': gql('''
    query getTopicCollectionPageRevision($id: ID) {
      all_page_revisions(id: $id) {
        edges {
          node {
            as_topic_collection_page {
              title
              slug
              description
              theme {
                slug
                text
                description
              }
            }
          }
        }
      }
    }
    '''),
    'topic': gql('''
        query getTopicPageRevision($id: ID) {
          all_page_revisions(id: $id) {
            edges {
              node {
                as_topic_page {
                  title
                  slug
                  description
                  topiccollections {
                    edges {
                      node {
                        topiccollection {
                          title
                          slug
                          description
                          theme {
                            slug
                            text
                            description
                          }
                          live_revision {
                            id
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
    '''),
    'information': gql('''
    query getInformationPageRevision($id: ID) {
      all_page_revisions(id: $id) {
        edges {
          node {
            as_information_page {
              title
              slug
              description
              topics {
                edges {
                  node {
                    topic {
                      title
                      slug
                      description
                      topiccollections {
                        edges {
                          node {
                            topiccollection {
                              title
                              slug
                              description
                              theme {
                                slug
                                text
                                description
                              }
                              live_revision {
                                id
                              }
                            }
                          }
                        }
                      }
                      live_revision {
                        id
                      }
                    }
                  }
                }
              }
              additional_content
              contacts {
                edges {
                  node {
                    contact {
                      id
                    }
                  }
                }
              }
              coa_global
            }
          }
        }
      }
    }
    '''),
    'services': gql('''
    query getServicePageRevision($id: ID) {
      allPageRevisions(id: $id) {
        edges {
          node {
            asServicePage {
              id
              title
              slug
              shortDescription
              dynamicContent
              steps
              topics {
                edges {
                  node {
                    topic {
                      id
                      title
                      slug
                      description
                      topiccollections {
                        edges {
                          node {
                            topiccollection {
                              id
                              title
                              slug
                              description
                              theme {
                                id
                                slug
                                text
                                description
                              }
                              liveRevision {
                                id
                              }
                            }
                          }
                        }
                      }
                      liveRevision {
                        id
                      }
                    }
                  }
                }
              }
              additionalContent
              contacts {
                edges {
                  node {
                    contact {
                      id
                    }
                  }
                }
              }
              coaGlobal
            }
          }
        }
      }
    }
    '''),
}
