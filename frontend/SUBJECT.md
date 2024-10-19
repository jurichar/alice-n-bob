Alice & Bob - Cloud take-home assignment - FRONTEND
==================================

# Objective

The goal of this assignment is to evaluate your ability to bootstrap a React project, make reasonable design choices, and effectively communicate about your work.

In short, you should feel comfortable sharing this implementation with your teammates and requesting a code review.

# Your Task

In this assignment, you will implement a React application that acts as the frontend for the Drone delivery API that you have already developed.

## Setup

Ensure that you have Node.js and npm installed on your machine, and that npm is accessible in your bash environment under the name `npm`.

In the `drone-delivery-frontend/` directory, we provide a skeleton of a React application that uses the Material UI component library.

To install the dependencies:

```bash
cd drone-delivery-frontend
npm install
```

To launch the frontend:

```bash
cd drone-delivery-frontend
npm start
```

Your implementation should replace or update the code in the `drone-delivery-frontend/` folder.

## Requirements

The React application should meet the following requirements:

1. **Dashboard**:
    - Create a dashboard that lists all ongoing deliveries.
    - Each delivery should display its current status (`PARCEL_COLLECTED`, `TAKEN_OFF`, etc.) and a unique delivery ID.
    - Implement a refresh button to manually update the list of ongoing deliveries.

2. **Delivery Details**:
    - When clicking on a specific delivery from the dashboard, display more detailed information (status, history of events, etc.).
    - If the delivery is completed (either `PARCEL_DELIVERED` or `CRASHED`), indicate this clearly.

3. **Delivery Tracking**: 
    - Implement a form that would allow to track any delivery by manually entering the ID (**including completed deliveries**) and access the details as described above.

4. **Add Events**:
    - Implement a form to send new events for a specific delivery (e.g., `POST /deliveries/delivery-id/events`). The form should allow the user to select the event type and submit it to the API.

5. **Statistics**:
    - Create a statistics section that shows the number of ongoing deliveries and the total number of deliveries since the start (using the `GET /counts` API).

6. **Responsiveness**:
    - Ensure the interface works well on different screen sizes (desktop and mobile).

## Bonus

- **Error Handling**: Display meaningful messages when there are issues connecting to the API (e.g., network errors, invalid responses) or when trying to track a delivery that does not exist.


# What We'll Evaluate

Beyond correctness, we expect your code to be production-ready. You should feel confident enough in your code to present it to your teammates and request a review.

We will pay particular attention to:

- Readability (structure, ease of use, comments, managing complexity)
- Maintainability (modularity, avoiding repetition)
- Pragmatism (using existing solutions when appropriate, conciseness)

**Please try to limit your effort to half a day's work once you start coding.** If you cannot finish within that time, we recommend stopping and outlining next steps in your README. We will take this into account during our evaluation!

Please submit your solution as an archive or a private Git repository. In the case of a private Git repository, please ask your Alice & Bob recruiter for the email addresses with which it should be shared.
