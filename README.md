# Half-empty
## the pessimists to-do app

Half-empty is a task management app for pessimists and misanthropes. Are you tired of toxic positivity but you still have things to get done? Than this app is for you! There are many task management apps out there, but this one in addition to being feature rich, has a sense of humor.

### Usage

In order to use Half-Empty you must register for an account. From there you will be taken to the index view where you can see "Today's list of meaningless tasks." Near of the top of the page you will see a random Demotivational Quote. If you don't like the quote you can hover underneath the quote and a "Boring.." button will appear. You can click this button to bring up a new quote.

This app was developed for Google Chrome. Though full support for other browsers is planned in the future, for now it is recommended that you use Chrome as some features may not work perfectly in other browsers.

#### Quick add

Underneath the quote you will see the quick search bar. Here you can type in the name of a task and it will be added to today's task list, or the the day that you have selected. You can select a new day via the pagination buttons or datepicker.

#### Detailed add

Near the bottom of the screen you will find the detailed add button, which will allow you to enter a task title, description (using the Quill rich text editor), label, and date. You can also choose to share the task with another user. See more about sharing tasks below.

#### Sharing tasks

You can specify a user to share a task with when you add or edit a task. For now you have to share with one person at a time, but you can share with as many users as you like. Sharing a task with a user for the first time will send them a request that they can accept or decline. If they accept they will see the shared tasks (as well as all future shares) and if they decline they will not see tasks that you share with them.

#### Editing tasks

Clicking on any task will bring up a drop down menu where you can make changes to the title, notes, label, or date. You can also choose to share the task with additional users. You will also find the "Open as page" button which will bring up the task in a full page view for more detailed descriptions. If the task in today's view, you will see a "Not today" button which quickly moves the task to tomorrow.

#### Checking off tasks

When you are done with a task, just check the checkbox. The task will be crossed off and after a short delay it will disappear from your screen. This allows you a second to uncheck it in case you made a mistake. If you need to uncheck a task after this or you just want to see what tasks you've completed, click the Logbook button in the navigation menu.

#### Account

In the nav menu you will see a button that says "Hey {username}." This links to your account page. There you can add, edit, or delete labels, share or unshare with other users, create a custom theme, change your password, or delete your account.


### Python files

#### views.py

This contains the logic for the various paths of the application. This includes but is not limited to the functions for viewing, adding, and editing tasks, as well as creating labels, custom themes, and many more features.

#### urls.py

This lists the paths for accessing the applications as views as well as adding, deleting, and updating data.

#### models.py

This page defines the models that are used to store the data for the app. These include User, Task, Tag, SharedTask, and Friend. 


### Templates

#### layout.html

This sets up the basic layout of the application including the navigation menu. The app is mobile responsive and there are sepereate menus for the desktop and mobile versions.

#### index.html

This template is used for various views to view tasks for the selected days and tag filter.

#### logbook.html

This template lists the users completed tasks.

#### account.html

The account page contains forms where the user can add, change, or delete labels, manage their sharing, create a custom theme, change their password, or delete their account.

#### page.html

This template is used the view a selected task as a full page. The task details can be edited on this page.

#### login.html and register.html

These pages just contain forms to login or register for a new account.


### Static files

#### procratinate.scss, procrastinate.css

I wrote the styles for the application in sass (procrastinate.scss), which compiles to procrastinate.css

#### procrastinate.js

This file contains the majority of the JavaScript for the front-end for the sight. This inlcudes function to make Fetch API calls to the server to add, edit, and recieve data, manipulate the style of the site, and trigger animations when tasks are checked off.

#### react.js

This file contains JSX and the React Component that is used to add new tasks.


### Libraries

Half-Empty uses Bootstrap to help style the app, React to create and render task components, and Quill to render rich text editors. Many icons from Font Awesome were also used. 






