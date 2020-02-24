<!-- # Title --> 
# Use department group permissions in place of related Department models

## Status
<!-- What is the status, such as proposed, accepted, rejected, deprecated, superseded, etc.? -->
Accepted

## Context

<!-- What is the issue that we're seeing that is motivating this decision or change? -->
Previously, we had pages assigned to department essentially by relating them to department pages. However, this caused problems, especially marking a page as belonging to a department if the page didn't exist, for example.

## Decision

<!--  What is the change that we're proposing and/or doing? -->

We remove department relations from their respective models.

Instead, we associate each page with belonging to a department group, either picked by an admin or associated by the department the user who creates the page belongs to.

## Consequences

<!-- What becomes easier or more difficult to do because of this change? -->

Generally speaking, this move cleans up our code a bit while also allowing for more permissions-based functionality. There aren't any obvious significant downsides, and it streamlines the codebase a bit.

Consequences to performance of the author app or builds is unknown.

### Things made easier
* If a page is associated with multiple departments, they all will be able to be queried by our API and shown on the frontend.
* New functionality for restricting user views by department is made possible, and that means less stuff for authors to have to look at, which is a better UX.
* Fewer resolvers need to be built/maintained for our GraphQL API

### Things made harder
* We need to create departments from pages as a data migration to make existing relationships propagate.
    * This is already done, so not really a big deal.   
* We don't have any automated tests in place to verify this change
    * At this early stage of the project, it dosen't seem like a big deal.
