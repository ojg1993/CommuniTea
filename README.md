<div align="center">
  <img src="https://github.com/ojg1993/CommuniTea/assets/61238157/9a211dc3-4c42-4051-b01c-cb81e1094302" alt="CommuniTea logo">
  <h1 align="center">CommuniTea</h1>
</div>

CommuniTea is a community platform designed for immigrants residing in the United Kingdom. It serves as a hub for sharing valuable information related to jobs, housing, restaurants, and more. This platform aims to connect individuals and foster a supportive environment for the immigrant community.

## Project Demo

Watch a quick demonstration of CommuniTea in action

[![CommuniTea Demo](https://example.com/demo_thumbnail.png)](https://example.com/demo_video.mp4)

This demo showcases key features, such as user authentication, post management, like interaction, and more. Follow along to see how CommuniTea can benefit you!

## Project Overview
### Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, Javascript
- **Backend:** Django
- **Database:** PostgreSQL
- **Deployment:** Docker, AWS

### Backend Architecture
diagram position

### Data Modeling

![datamodeling](https://github.com/ojg1993/CommuniTea/assets/61238157/c19a8784-77e9-4dd5-bd90-39d9a9c1d251)

### UI/UX Prototype Design

![ui-ux prototype](https://github.com/ojg1993/CommuniTea/assets/61238157/b78834be-e3b3-4b59-9d08-466ef1499df7)

### Features

#### User Authentication and Account Management

- **AbstractUser Implementation:** Utilized `AbstractUser` for email login, applying a custom user model (`CustomUser`).
- **Account Creation and Email Verification:** Implemented a Google App-based email verification process following account creation.
- **Account Information Management:** Dropdown button for account modification and deletion.

#### Post Management

- **Post CRUD Operations:**
  - Create, read, update, and delete posts.
  - Post actions restricted to logged-in users (`login_required` decorator).
- **Category-specific Post Viewing:**
  - View posts by category (e.g., all, best, open forum) with pagination.
  - Sort 'best' category based on likes and views.

#### Comment Management

- **Comment CRUD Operations:**
  - Create, read, update, and delete comments.
  - Comment actions restricted to the comment author.

#### Interaction and Notification Features

- **Like and Dislike Functionality:** Users can express emotions through likes and dislikes, choosing only one.
- **MyPage Feature:**
  - Overview of posts and comments created by the user with paginated results.
- **Integrated Search Feature:** Search for posts based on keywords in the author, title, or content with paginated results.
- **Notification Features:** Popup notifications for actions such as post creation, modification, and empty search results, disappearing after 2.5 seconds.

## Installation

- installation instruction

## Getting Started

- running application instruction
