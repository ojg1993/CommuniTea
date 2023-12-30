<div align="center">
  <img src="https://github.com/ojg1993/CommuniTea/assets/61238157/9a211dc3-4c42-4051-b01c-cb81e1094302" alt="CommuniTea logo">
  <h1 align="center">CommuniTea</h1>
</div>

CommuniTea is a community platform designed for immigrants residing in the United Kingdom. It serves as a hub for sharing valuable information related to jobs, housing, restaurants, and more. This platform aims to connect individuals and foster a supportive environment for the immigrant community.

## Project Demo

Watch a quick demonstration of CommuniTea in action !
<br>
<br>

<div style="display: flex; justify-content: space-between;">
    <div style="text-align: center;">
        <span>Register / Authentication / Email verification & Password reset / User update & delete</span>
        <br>
        <br>
        <img src="https://github.com/ojg1993/CommuniTea/assets/61238157/1aa62dc5-5608-46d5-817e-e30af73d4bda" width="400">
    </div>
    <br>
    <br>
    <div style="text-align: center;">
        <span>Post & Comment CRUD / Post navigation / Post & Comment pagination</span>
        <br>
        <br>
        <img src="https://github.com/ojg1993/CommuniTea/assets/61238157/ff485c19-0451-486a-bc44-44e4ae2e59ba" width="400">
    </div>
    <br>
    <br>
    <div style="text-align: center;">
        <span>Search / Like & Dislike / Hits / Best / My page</span>
        <br>
        <br>
        <img src="https://github.com/ojg1993/CommuniTea/assets/61238157/e63b43e3-6203-4278-a21f-7ed8764dd237" width="400">
    </div>
</div>

## Project Overview
### Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, Django, Javascript
- **Backend:** Django
- **Database:** PostgreSQL
- **Deployment:** Git Actions, Docker, AWS Elastic Beanstalk
- **Version Control:** Git, Github

### Backend System Architecture
![backend system architecture](https://github.com/ojg1993/CommuniTea/assets/61238157/dccd4923-0243-49b4-80c8-89e6c8dab203)

### Data Modeling

![data modeling](https://github.com/ojg1993/CommuniTea/assets/61238157/47c803b0-89c0-470c-bd13-3f9cc1927030)

### UI/UX Prototype Design

![ui-ux prototype](https://github.com/ojg1993/CommuniTea/assets/61238157/b78834be-e3b3-4b59-9d08-466ef1499df7)

### Features

#### User Authentication and Account Management

- **AbstractUser Implementation:** Utilized `AbstractUser` for email login, applying a custom user model (`CustomUser`).
- **Account Creation and Email Verification:** Implemented a Google App-based email verification process following account creation.
- **Account Information Management:** Dropdown button on `My Page` for account modification and deletion.

#### Post Management

- **Post CRUD Operations:**
  - Create, read, update, and delete posts.
  - Post actions restricted to logged-in users.
- **Category-specific Post Viewing:**
  - View posts by category (e.g., all, best, open forum) with pagination.
  - Sort 'best' category posts based on likes and views.

#### Comment Management

- **Comment CRUD Operations:**
  - Create, read, update, and delete comments.
  - Comment actions restricted to the comment author.

#### Interaction and Notification Features

- **Like and Dislike Functionality:** Users can express emotions through like or dislike button.
- **MyPage Feature:** Overview of posts and comments created by the user with paginated results.
- **Integrated Search Feature:** Search for posts based on keywords in the author, title, or content with paginated results.
- **Notification Features:** Popup notifications for actions such as Login / Logout and CRUD events disappearing shortly.

## Challenges & Solutions
During the development of this project, I faced some issues that needed careful solutions. Here, sharing the main difficulties encountered and the strategies used to overcome them.

### Challenge 1: [Anonymous User displayed in templates after successful Login]

#### Problem Description:
After implementing an email-based login using a custom user model (AbstractUser), BaseUserManager, and a custom ModelBackend, an issue emerged. Upon successful login, the ***template displayed {{ request.user }} as an anonymous user***.

### Solution:

1. **Understanding AbstractUser and Custom User Model**:
Initially, I explored the official documentation and conducted thorough Google searches to grasp the details of the AbstractUser class and the custom user model. Despite these efforts, the issue persisted.

2. **Focusing on ModelBackend**:
Realizing that the problem might not be within the custom user model, I shifted my focus to the custom ModelBackend used for authentication. Despite exploring official documentation, online searches, and community forums extensively, a solution remained elusive.

3. **Customizing ModelBackend's get_user Method**:
In a breakthrough moment, I carefully reviewed the methods provided by ModelBackend. By customizing the get_user method within the EmailBackend class, I successfully resolved the issue.

### Conclusion:
The journey involved a detailed examination of different components, ultimately leading to the realisation that the solution lay in customizing the ModelBackend's get_user method. Despite initial challenges and extensive research, grasping the details of the authentication backend proved crucial in achieving success.

### Challenge 2: [Designing backend system architecture]

#### Problem Description:
In the deployment phase of my application, I encountered confusion regarding the roles of Web server, WSGI server, and App server. The detailed aspects of their responsibilities, particularly the communication flow involving Nginx, Gurnicorn, and Django app, needed clarification. Additionally, my goal was to containerize the application using Docker and deploy it through AWS Elastic Beanstalk. However, the automatic setups done by AWS Elastic Beanstalk were unclear to me. The deployment process seemed overwhelming, leading to research through Google searches and references to alternative architectures.

### Solution:

1. **Understanding Server Roles:**
   - **Web Server (Nginx):** The entry point for user requests, initiating the communication process flow.
   - **WSGI Server (Gunicorn):** An intermediary facilitating smooth communication between the web server and the app server.
   - **App Server (Django):** The core of the web application, handling user requests and generating responses by coordinating view logics with other components.

2. **Deployment with AWS Elastic Beanstalk and Docker:**
   - **AWS Elastic Beanstalk:** A user-friendly Platform-as-a-Service (PaaS) solution designed for simple and swift deployment. It also takes care of configuring related environments, including EC2 with Auto Scaling options, Load Balancer, and more.
   - **Docker:** Packing up all the essentials of the app needs(code, libraries, and settings) into a container. Meaning the app behaves consistently no matter where it goes.
<br><br>
   ***AWS Elastic Beanstalk*** serves as a helpful assistant, smoothly handling the deployment of the ***Docker image***. It simplifies the entire process, making it easy to manage and deploy the app without getting stuck with excessive details.
### Conclusion:
The exploration of server roles and the deployment process, which involves AWS Elastic Beanstalk and Docker, played a pivotal role in simplifying the details of application deployment. Understanding the communication flow and utilizing Docker in conjunction with the user-friendly features of AWS Elastic Beanstalk contributed to a more straightforward deployment experience.
