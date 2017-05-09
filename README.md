*** Discrete Math Course Dictionary ***

# Background

Similar to: #102

Learning by googling some time faster than reading a book. however, googling for basic courses is not really efficient and effective because they usually give more answer than we need. Most of the time, for basic courses such as Discrete Math or Linear Algebra, following the lecture notes and the given text book is better. 

It is also probably helpful to have terminology references while discussing some concept with your friend.

# Description

N/A
 
# Definition of Done

- [ ] Create a database of dictionary in JSON format as a flat text file.  
    - The format should at least consists of:
    ```
    Course (e.g Discrete Math),
    Keyword (e.g. relation), 
    Definition (e.g. definition of relation), 
    Example (e.g example of some relation), 
    Ref (e.q. chapter in the text book for further reading),
    Problem (e.g. example of related problem in exam or quiz)
    ```
- [ ] Provide command to query. For example: `/tellme relation`
    - The bot will nicely render the answer by using layout, colour and typesetting appropriately. 
    If the data about relation is not available, the bot answer nicely, for example: 
    No one has told me about relation, please ask someone to add it in our knowledge base.
- [ ] WIP contained in a branch and tracked in GitLab repository
- [ ] Created or worked a module specific for containing functionalities related to this user story
- [ ] Wrote stubs & unit tests
- [ ] Test coverage >= 70%
- [ ] Provided error handling for boundary cases and other exceptional cases
- [ ] Build passed (i.e. not failed)
- [ ] Have tested the working build on Heroku instance