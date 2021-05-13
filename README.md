# camagru
#### A web application allowing you to make basic photo and video editing using your webcam and some predefined images

To launch the project execute
```shell
docker compose up
#OR
docker-compose up
```

Or without docker
```shell
python mysite/manage.py runserver --insecure
```
> `--insecure` is needed so that Django's built-in server will continue serving static files if DEBUG is set to False in settings.py. If you set DEBUG to True you can remove it.

---
## General
- [x] responsive design
    - desktop
    - mobile
    - bootstrap (bonus)
## User features
<img width="1340" alt="Screen Shot 2021-05-13 at 10 17 33" src="https://user-images.githubusercontent.com/27923828/118099865-1c0e3b00-b3d6-11eb-869b-5c252297c9ee.png">
<img width="1340" alt="Screen Shot 2021-05-13 at 10 18 23" src="https://user-images.githubusercontent.com/27923828/118099955-334d2880-b3d6-11eb-9ea9-532876c9911c.png">

- [x] sign up, sign in, sign out
- [x] confirm account by email
- [x] forgot password (reset it by email)
- [x] settings view
    - user can modify it's profile
    - email notifications: (un)subscribe if someone leaves a comment on user's picture(s)
    - delete account (bonus)

## Gallery features
<img width="868" alt="Screen Shot 2021-05-13 at 10 20 08" src="https://user-images.githubusercontent.com/27923828/118100185-73aca680-b3d6-11eb-88e3-a759f154050d.png">

- [x] display all the images edited by all the users, plus likes and comments for everyone
- [x] let signed in users (un)like and leave comments
- [x] pagination: 5 images per page

## Editing features
<img width="1259" alt="Screen Shot 2021-05-13 at 10 26 35" src="https://user-images.githubusercontent.com/27923828/118100260-8aeb9400-b3d6-11eb-801d-56ceb58b4165.png">
<img width="1259" alt="Screen Shot 2021-05-13 at 10 27 09" src="https://user-images.githubusercontent.com/27923828/118100325-9ccd3700-b3d6-11eb-8d12-9f339841bc40.png">

- [x] accessible only to signed in users
- [x] main section
    - preview of the user’s webcam (if it has one)
    - possibility to upload a picture
    - overlays to apply over the original picture
- [x] side section 
    - thumbnails of all previous pictures taken
    - delete picture button
    - possibility to select previous picture for further editing (bonus)
- [x] creation of the final image is done on the server side.
