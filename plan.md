# Postly DRF API

`TLDR` Develop the simple DRF API which would be used for posting the Posts like its in different social media platforms, as well as comment and like the posts. (add the email verification method before sign up)

## Setting up the Project

1. Setup the django application and provide the only way to login using email and password, and also provide a way to login with google (if you would have time). - ___OK___
2. Change the in-built django model for creating the email as a primary key and removing username field from the User model. - ___OK___
3. Test the modified User Model using Django API Client and pytest. - ___OK___
4. Find out a way to send the code to user email for verification before signing up, in order to prevent the registrations using fake emails.
5. Setup that smtp or what so ever emailing method.
6. Test that method by creating the user inside admin panel if its valid over there, or create some view to test it.
7. Test it using Django API Client and Pytest.

## Creating Rest API and setting up the user login methods

1. First of all Develop the sign up method for the user using drf after that email verification.
2. create user model serializer for the views to signup and login the user
3. Develop user modelviewsets for sign up and logging in the user.
4. Test these views using post and get methods from web api and using django client and pytest as well. create separate test classes for each view as well.
5. Check if email verification code is being received or not and either user are created successfully.
6. Check if how would it be retained for the rest of the time. Also test views using Postman to check its real behavior as an api.

## Adding posts for the user

1. Create the model for the Posts as well for the comments of those posts, and related models as well, like model, dislike model and picture model.
2. Also you need to setup the cloudinary account and integrate it with your project for saving the pictures of the post.
3. as you take the foreign key of the picture inside the post, so you would also have to create the Picture Model.
4. first add the way for the single picture inside the post as cloudinary image field, and the add the support for multiple pictures after it would be working fine inside the posts model.
5. check it using django admin
6. Post Model would be having the following fields.

   - Title (Character field with max length of 75)
   - author (Foreign key for the User model) along with related name for the reverse look up.

    Pictures, first create them using simple django cloudinary field for the testing purposes and then modify the model to pictures which field would be removed from this Model and another Pictures Model would be created with relevant fields. and post would be Foreign Key over there.
   - Content (TEXT Field)
   - created at (Datetime field)
   - modified at (datetime field)
   - Views on the post (Bigint field and default to 0)
   - likes counts (bigint field with default to 0) and increased using action methods and required would False and would be calculated using aggregate queryset for the action method
   - dislikes counts (bigint field with default to 0) and increased using action methods and required would False and would be calculated using aggregate queryset for action method

7. Comment model would be having these fields

   - author (foreign key for the user) also add the related name
   - content (Text field)
   - commented_at (datetime field)
   - edited at (datetime field)
   - post (forign key for the post model) & its related name

8. Picture Model which would be created after the cloudinary integration testing, would be having following fields

   - picture (imagecloudinaryfield) and used properly after proper configurations
   - post (foreign key for the post) and its related name

    > Note: we would be adding the abstract class for like and dislike model as components are open for extension but close for modification according to SOLID Principles, so we can't modify the like model for dislike model

9. AbstractLikeDislikeModel
    This model would not have any table nor migrations, as its abstract class
    - reactor
    - post

10. Like Model (inherits from AbstractLikeDislikeModel)

    - liked (boolean field) default to False
    SO, its other fields would reactor and post

11. Dislike Model (inherits from AbstractLikeDislikeModel)

    - disliked (boolean field) default to False
    So its other fields would also reactor and post

12. Test these models using django admin after registering.
13. Create the tests of all of these models using django api client and pytest one by one.
14. create the specific and suitable model serializer for the post which would be working properly for all of the fields.
15. even create the different serializers for list, create operations and retrieve, update and destroy operations.
16. test these serialzers after creating that whether they are working properly.
17. first test them pytest and then using django_api/pytest
18. create the the viewsets and routers for the post with the specific querysets, permission and authentication classes.
19. also add the action methods for like, dislike and views. using separate and proper query sets.
20. test them using web api and also using pytest/django_api
21. also add the filtering and pagination support for the posts.
22. so all the aspects required would be covered
23. add the django cors headers after the integration with frontend ui using this lib [django-cors-headers](https://pypi.org/project/django-cors-headers/)

Integrate it with the downloaded ui properly.
