import http from 'k6/http';
import { sleep } from 'k6';
export let options = {
  vus: 10,
  duration: '30s',
};

let query = `
{
  pages {
    ...on OfficialDocumentPage {
      documents {
        id
        name
        date
        title
        authoringOffice
        summary
        name
        document {
          file
          fileSize
          fileHash
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
    'https://joplin-pr-try-grapple-no-redis.herokuapp.com/graphql',
    JSON.stringify({ query: query }),
    { headers: headers }
  );

  check(res, {
    'is status 200': (r) => r.status === 200,
    'body size is 314968 bytes': (r) => r.body.length == 314968,
  });
}
