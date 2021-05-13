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
python mysite/manage.py runserver 0.0.0.0:8000 --insecure
```
> `--insecure` is needed so that Django's built-in server will continue serving static files if DEBUG is set to False in settings.py. If you set DEBUG to True you can remove it.

---
## User features
- [x] sign up, sign in, sign out
- [x] confirm account by email
- [x] forgot password (reset it by email)
- [x] settings view
    - user can modify it's profile
    - email notifications: (un)subscribe if someone leaves a comment on user's picture(s)
    - delete account (bonus)

## Gallery features
- [x] display all the images edited by all the users, plus likes and comments for everyone
- [x] let signed in users (un)like and leave comments
- [x] pagination: 5 images per page

## Editing features
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