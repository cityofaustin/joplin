# Joplin UI Developement Notes

NOTE: This readme was created during the great redesign of 2020.
- I (Bob) created these notes and guidelines once I developed a pattern during the build-out of the new design.
- I'm sorry. I know it's messy. I'll clean it up as I go along. 

### Joplin UI: general workflow and development with wagtail templates

Here are a set of "guidelines" I created for myself when developing the Joplin UI.

- Only modify the html of templates by adding specific `coa-` prefixed class names and ids and style them within the `/joplin_UI` folder.
  - This way, a fallback to any original wagtail styles is always in place, as we're "modifying" the css, rather than building our own css from scratch.
  - It also keeps the specific style code isolated and easily referenced against any wagtail specific styles being done.
  - Here's an example:
```css
  #coa-primary_navigation .nav-main .menu-active {
    background-color: $coa-background-color-secondary;
    text-shadow: none !important;
  }
```
  - Here we'ved added `id="coa-primary_navigation"` to a template element and modifying its decedents with classes of `.nav-main` and `.menu-active`.
  - Sometimes, depending on render order, the `!important` tag may need to be applied, though, it's worth investigating a bit to see why.
- Add an `id` to the top parent of any modified templates.
  - By doing this you can often get away with only adding that id to the template and then style decedents when it makes sense. Example: `#coa-sidebar .inner a { ...`
- "Pull up" wagtail core templates when needed to add specific ids and classes.
  - Sometime when modifying our css, we find that the template and element do not exist within our code base. So, we need to find the template within the wagtail admin and add it to our existing code base within the same directory.
  - Example: We need to change a specific style of an element. We then discover, after inspecting, that it has a class of `listing-filter`. However, when we search our code-base, we do not find the html element where the class is applied.
  - This usually means the template is within wagtail's admin code base, so we need to add the file to _our_ code base to modify the html.
  - We can search our own wagtail code within our library, or here's an example search result from within wagtails github: https://github.com/wagtail/wagtail/search?q=listing-filter&unscoped_q=listing-filter
  - We now have found the correct class and can create a new file in our code base in the same location, with the same name that houses the same code!
  - And, django + wagtail know to use our code instead of the file from the library.
  - so now we can add a specific `coa-listing-filter` class and style that class within a corresponding .scss file.
- Be as unobtrusive to the original state as possible, and inject new code with spacific documentation when needed.
