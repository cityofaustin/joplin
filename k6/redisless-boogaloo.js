import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';
export let options = {
  vus: 10,
  duration: '100s',
};

let query = `
{
  allPages {
    edges {
      node {
        janisbasepagewithtopics {
          officialdocumentpage {
            documents {
              edges {
                node {
                  title
                  id
                  document {
                    filename
                    fileSize
                  }
                  documentEs {
                    filename
                    fileSize
                    fileHash
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}`;

let headers = {
  'Content-Type': 'application/json',
};

export default function() {
  let res = http.post(
    'https://joplin-pr-redisless-boogaloo.herokuapp.com/api/graphql',
    JSON.stringify({ query: query }),
    { headers: headers }
  );

  check(res, {
    'is status 200': (r) => r.status === 200,
    'body size is 261559 bytes': (r) => r.body.length == 261559,
  });
  // console.log(res.status);

  // if (res.status === 200) {
  //   console.log(JSON.stringify(res.body));
  // }
}
