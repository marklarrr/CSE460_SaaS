from django.template import RequestContext
from django.shortcuts import render_to_response
from saas.models import Category, Page, UserProfile
from saas.forms import UserForm, UserProfileForm, addProjectForm, addRequirementForm, addManagerForm, addWorkerForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
    
def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    # Query for categories - add the list to our context dictionary.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    # Render the response and return to the client.
    return render_to_response('saas/index.html', context_dict, context)

def category(request, category_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    category_name = category_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'category_name': category_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(name=category_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('saas/category.html', context_dict, context)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'saas/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.

        all_tenants = UserProfile.objects.all()
        print all_tenants

        for e in all_tenants:
            test = e.user.username
            if user is not None:
                if username == test:
                    if user.is_active:
                        login(request,user)
                        print "going to tenanthome"
                        return HttpResponseRedirect('/saas/Tenanthome')
                # # Is the account active? It could have been disabled.
                # elif user.is_active and username != test:
                #     # If the account is valid and active, we can log the user in.
                #     # We'll send the user back to the homepage.
                #     login(request, user)
                #     return HttpResponseRedirect('/saas/login')
                # else:
                #     # An inactive account was used - no logging in!
                #     return HttpResponse("Your account is disabled.")
            else:
                # Bad login details were provided. So we can't log the user in.
                print "Invalid login details: {0}, {1}".format(username, password)
                return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('saas/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/saas/login')

def addProject(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        addProject_form = addProjectForm(data=request.POST)

        # If the two forms are valid...
        if addProject_form.is_valid():
            # Save the user's form data to the database.
            project = addProject_form.save()
            project.save()


        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print addProject_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        addProject_form = addProjectForm()

    # Render the template depending on the context.
    return render_to_response(
            'saas/addProject.html',
            {'addProject_form': addProject_form},
            context)

def addRequirement(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        addRequirement_form = addRequirementForm(data=request.POST)


        # If the two forms are valid...
        if addRequirement_form.is_valid():
            # Save the user's form data to the database.
            project = addRequirement_form.save()
            project.save()


        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print addRequirement_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        addRequirement_form = addRequirementForm()

    # Render the template depending on the context.
    return render_to_response(
            'saas/addRequirement.html',
            {'addRequirement_form': addRequirement_form},
            context)

def addManager(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        addManager_form = addManagerForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and addManager_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = addManager_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()


        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, addManager_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        addManager_form = addManagerForm()

    # Render the template depending on the context.
    return render_to_response(
            'saas/addManager.html',
            {'user_form': user_form, 'addManager_form': addManager_form},
            context)

def addWorker(request):
    # Like before, get the request's context.
    context = RequestContext(request)



    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        addWorker_form = addWorkerForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and addWorker_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = addWorker_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()


        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, addWorker_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        addWorker_form = addWorkerForm()

    # Render the template depending on the context.
    return render_to_response(
            'saas/addUser.html',
            {'user_form': user_form, 'addWorker_form': addWorker_form},
            context)

def tenantHome(request):
    context = RequestContext(request)

    current_user = request.user.username

    tenant_list = UserProfile.objects.all()
    service_list = []

    for e in tenant_list:
        test = e.user.username
        if current_user == test and current_user:
            if tenant_list.filter(addproject = 1):
                service_list.append("addProject")
            if tenant_list.filter(addRequirements = 1):
                service_list.append("addRequirements")
            if tenant_list.filter(modifyProjectStatus = 1):
                service_list.append("modifyProjectStatus")
            if tenant_list.filter(viewReqStatus = 1):
                service_list.append("viewReqStatus")
            if tenant_list.filter(viewProjectsManager = 1):
                service_list.append("viewProjectsManager")
            if tenant_list.filter(modReqStatus = 1):
                service_list.append("modReqStatus")
            if tenant_list.filter(viewAssignedReqs = 1):
                service_list.append("viewAssignedReqs")

    print service_list



    return render_to_response('saas/Tenanthome.html',context)