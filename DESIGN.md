# Wollongong Coffee

## Requirements

### Function requirements

| #   | As a           | I want to                                                          | So that           |
| --- | -------------- | ------------------------------------------------------------------ | ----------------- |
| 1   | Coffee drinker | Find best cafe nearby                                              | Get a good coffee |
| 2   | Coffee drinker | Find best cafe nearby even if have not tried any cafes in the town | Get a good coffee |
| 3   | Coffee drinker | Make sure only I can see my recommendations                        | I feel secure     |

### Performance requirements

| #   | Requirement type | Requirement                        | Measure                              | Unit of measure | Goal | Minumum | Maximum |
| --- | ---------------- | ---------------------------------- | ------------------------------------ | --------------- | ---- | ------- | ------- |
| 1   | Usability        | Support quick sign up              | Number of questions in questionnaire | count           | 3    |         |         |
| 2   | Usability        | Support quick sign up              | Number of cafe rankings to enter     | count           |      | 0       |         |
| 3   | Performance      | Support quick first recommendation | Wait before 1st recommendation       | seconds         | 5    |         | 10      |
| 4   | Maintainability  | Quick set up by developers         | Time to set up project from scratch  | minutes         | 30   |         |         |
| 5   | Scalability      | Support sufficient number of users | Number of users                      | count           | 100  | 5       | 1000    |
| 6   | Scalability      | Support sufficient number of cafes | Number of cafes in Wollongong        | count           | 100  | 10      | 1000    |

#### References

https://www.nngroup.com/articles/response-times-3-important-limits/

### Constraints

| #   | Constraint type      | Requirement         |                                                           |
| --- | -------------------- | ------------------- | --------------------------------------------------------- |
| 1   | Legal and compliance | Don't store any PII | Otherwise we need to follow Australian Privacy Principles |

## Design

### Components

TODO: Diagram

### Interactions

### Design decisions

#### Decision 1

| Attribute          | Text                                                                                |
| ------------------ | ----------------------------------------------------------------------------------- |
| #                  | 1                                                                                   |
| Design decision    | Recalculate recomendations one user at a time on registration                       |
| Rationale          | To make sure recommendations are available quickly - see requirement 3              |
| Trade-offs         | Extra complexity as need to recalculate on registration or sign in and periodically |
| Options considered | Recalculate for everyone nightly                                                    |
| Notes              |                                                                                     |

#### Decision 2

| Attribute          | Text                                                                                   |
| ------------------ | -------------------------------------------------------------------------------------- |
| #                  | 2                                                                                      |
| Design decision    | Don't store any PII.                                                                   |
| Rationale          | We don't want to deal with Australian Privacy Principles, etc.                         |
| Trade-offs         | We can't email people and ask questions, etc.                                          |
| Options considered | Use email and comply, but's complicated. Use Google, MS, FB or other identity provider |
| Notes              |                                                                                        |

#### Decision 3

| Attribute          | Text                                                                      |
| ------------------ | ------------------------------------------------------------------------- |
| #                  | 3                                                                         |
| Design decision    | Add "Skip" button so people don't need to provide cafe rankings up front  |
| Rationale          | So quality of data is high, otherwise people will just enter garbage      |
| Trade-offs         | More complex model (we need clustering, etc. etc.)                        |
| Options considered | Google timemeline, but thats complex and expensive and people may opt out |
| Notes              |                                                                           |

#### Decision 4

| Attribute          | Text                                                                                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| #                  | 4                                                                                                                       |
| Design decision    | As soon as people fill any part of the survey, we need to assign them to a group and start calculating the cafe ratings |
| Rationale          | Performance requirements (we don't have time to wait until the rankins are submitted)                                   |
| Trade-offs         | More components, more complex system, more stuff to write (frontend and backend)                                        |
| Options considered | Fixed set of top cafes for a given location, but this may be too complicated (getting location off Google, etc.).       |
| Notes              |                                                                                                                         |

#### Decision 5

| Attribute          | Text                                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| #                  | 5                                                                                                                        |
| Design decision    | Use Docker Compose                                                                                                       |
| Rationale          | Developers can stand up the environent quickly                                                                           |
| Trade-offs         | We need to put it together, need to install Docker, need to know how to work with it, prerequisites need to be satisfied |
| Options considered | Bare metal set up, HDD image                                                                                             |
| Notes              |                                                                                                                          |

#### Decision 6

| Attribute          | Text                                                                                                                                                              |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| #                  | 6                                                                                                                                                                 |
| Design decision    | Use weighted average of two collaborative filtering model - one based on group where user belongs based on survey, another ranking based on provided cafe nakings |
| Rationale          | We need to deal with cold start problem (people click skip and don't rank cafes)                                                                                  |
| Trade-offs         | Less precise recommendations                                                                                                                                      |
| Options considered | Single model for collaborative filtering, but that creates cold start issues.                                                                                     |
| Notes              |                                                                                                                                                                   |

#### Decision 7

| Attribute          | Text                                                                                      |
| ------------------ | ----------------------------------------------------------------------------------------- |
| #                  | 7                                                                                         |
| Design decision    | Provide services and abstact all DB ML DB operations from what people are doing on the UI |
| Rationale          | Distributed team that rarely meets                                                        |
| Trade-offs         | Inefficiently in storage                                                                  |
| Options considered | One big database, but that is tricky to integrate                                         |
| Notes              |                                                                                           |

#### Decision 8

| Attribute          | Text                                                                                            |
| ------------------ | ----------------------------------------------------------------------------------------------- |
| #                  | 8                                                                                               |
| Design decision    | Collect initial data from questionare published over social media                               |
| Rationale          | We need data to build initial model                                                             |
| Trade-offs         | We are rebuilding application in a google form in effect                                        |
| Options considered | 1. Try to find dataset. 2. Start with empty database and collect data as people start using it. |
| Notes              | Dependencies: Question required. Cafe list required.                                            |

#### Decision 9

| Attribute          | Text                                                                                            |
| ------------------ | ----------------------------------------------------------------------------------------------- |
| #                  | 9                                                                                               |
| Design decision    | Collect cafes from the google maps api                                                          |
| Rationale          | We need data to build initial model                                                             |
| Trade-offs         | We are rebuilding application in a google form in effect                                        |
| Options considered | 1. Try to find dataset. 2. Start with empty database and collect data as people start using it. |
| Notes              | Dependencies: Question required. Cafe list required.                                            |


## Outstanding questions

1. Where are the cafe rankings that users enter on signing up? What rakings? Like/Did Not Like/Skip vs. Stars/Skip
2. How are rankings across different categories (ambiance, etc.) used on the Cafe Page?
