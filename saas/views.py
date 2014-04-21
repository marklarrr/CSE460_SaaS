from django.template import RequestContext
from django.shortcuts import render_to_response
from saas.models import Category, Page, UserProfile, Worker, Manager, Project, Requirement
from saas.forms import UserForm, UserProfileForm, addProjectForm, addRequirementForm, addManagerForm, addWorkerForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
    
def index(request):
    return render_to_response('saas/websitehomepage.html')

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

        for tenant in all_tenants:
            tester = tenant.user.username
            if username == tester:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect('/saas/Tenanthome')
                else:
                    return HttpResponse('Something went wrong')
        return HttpResponse('You are not a tenant')

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
    return HttpResponseRedirect('/saas/websitehomepage')

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
        if current_user == test:
            if  e.addproject == True:
                service_list.append("addProject")
            if e.addRequirements == True:
                service_list.append("addRequirements")
            if e.modifyProjectStatus == True:
                service_list.append("modifyProjectStatus")
            if e.viewReqStatus== True:
                service_list.append("viewReqStatus")
            if e.viewProjectsManager == True:
                service_list.append("viewProjectsManager")
            if e.modReqStatus == True:
                service_list.append("modReqStatus")
            if e.viewAssignedReqs == True:
                service_list.append("viewAssignedReqs")

    return render_to_response('saas/Tenanthome.html',
                              {'service_list': service_list},context)

def worker_login(request):
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

        all_workers = Worker.objects.all()

        for worker in all_workers:
            tester = worker.user.username
            if username == tester:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect('/saas/workerHome')
                else:
                    return HttpResponse('Something went wrong')
        return HttpResponse('You are not a worker')

    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('saas/WorkerLogin.html', {}, context)

def manager_login(request):
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
        all_managers = Manager.objects.all()

        for manager in all_managers:
            tester = manager.user.username
            if username == tester:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect('/saas/Dashboard')
                else:
                    return HttpResponse('Something went wrong')
        return HttpResponse('You are not a manager')

    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('saas/managerLogin.html', {}, context)

def Dashboard(request):
    return render_to_response('saas/Dashboard.html')

def workerHome(request):
    context = RequestContext(request)

    current_user = request.user.username

    requirement_list = Requirement.objects.all()
    worker_requirements = []

    worker_list = Worker.objects.all()

    for e in worker_list:
        user = e.user.username
        valid = e.tenant.viewAssignedReqs
        if current_user == user and valid == 1:
            for requirement in requirement_list:
                test = requirement.worker.user.username
                if current_user == test:
                    worker_requirements.append(requirement)

    return render_to_response('saas/workerHome.html',
                              {'worker_requirements': worker_requirements}, context)



























