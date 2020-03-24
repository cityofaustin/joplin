from gql import gql

queries = {
    'topiccollection': gql('''
    query getTopicCollectionPageRevision($id: ID) {
      allPageRevisions(id: $id) {
        edges {
          node {
            asTopicCollectionPage {
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
          allPageRevisions(id: $id) {
            edges {
              node {
                asTopicPage {
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
                }
              }
            }
          }
        }
    '''),
    'information': gql('''
    query getInformationPageRevision($id: ID) {
      allPageRevisions(id: $id) {
        edges {
          node {
            asInformationPage {
              id
              title
              slug
              description
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
