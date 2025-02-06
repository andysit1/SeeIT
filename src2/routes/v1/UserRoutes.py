# make routes to get user data
# make routes to get bin


# @router.post(
#     "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
# )
# def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
#     """
#     Create new user.
#     """
#     user = crud.get_user_by_email(session=session, email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this email already exists in the system.",
#         )

#     user = crud.create_user(session=session, user_create=user_in)

#     if settings.emails_enabled and user_in.email:
#         email_data = generate_new_account_email(
#             email_to=user_in.email, username=user_in.email, password=user_in.password
#         )
#         send_email(
#             email_to=user_in.email,
#             subject=email_data.subject,
#             html_content=email_data.html_content,
#         )
#     return user



# @router.get(reponse_model = user reponse)
# get reponse and return data.. forget about formating...

# change src2 to app cause wtf is src2...
  #make routes
#features todo tomorrow
  #this main stuff to do..

  #create user
    #given data

  #get user and bins

  #get bin and all media