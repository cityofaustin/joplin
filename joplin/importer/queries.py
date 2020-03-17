from gql import gql

queries = {
    'topiccollection': gql('''
    query getTopicPageRevision($id: ID) {
      allPageRevisions(id: $id) {
        edges {
          node {
            asTopicCollectionPage {
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
                    id
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
        query getInformationPageRevision($id:ID) {
          allPageRevisions(id:$id) {
            edges {
              node {
                asInformationPage {
                  id
                  title
                  topics {
                    edges {
                      node {
                        id
                      }
                    }
                  }
                  departments {
                    id
                  }
                  description
                  additionalContent
                  contacts {
                    edges {
                      node {
                        id
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
