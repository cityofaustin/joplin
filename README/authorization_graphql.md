## Why

We use the "django-graphql-jwt" library to enable authorization to make certain graphql requests. Graphql queries that request sensitive information like page owner data must now be authorized to do so.

An example of a query requiring authorization:
```
query getInformationPage($id: ID) {
  allInformationPages(id: $id) {
    edges {
      node {
        title       
        owner {
          id
          firstName
          lastName
          isSuperuser
          email

        }
      }
    }
  }
}
```

## How
https://django-graphql-jwt.domake.io/en/latest/authentication.html#http-header

Using a service like Insomnia, you can pass an Authorization Header with your graphql request.
`Authorization: JWT <token>`.

## Where do I get an authorization token?
Official Docs: https://django-graphql-jwt.domake.io/en/latest/quickstart.html

Slightly easier tutorial: https://www.howtographql.com/graphql-python/4-authentication/

Request a token by passing this mutation into graphql.

```
mutation TokenAuth($username: String!, $password: String!) {
  tokenAuth(username: $username, password: $password) {
    token
  }
}
```

Note: you must use a superuser's username and password in order to access data from resolvers that are `@superuser_required`.
