from django.template import RequestContext
from django.shortcuts import render_to_response
from saas.models import Category, Page, UserProfile, Worker, Manager, Project, Requirement
from saas.forms import UserForm, UserProfileForm, addProjectForm, addRequirementForm, addManagerForm, addWorkerForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
    
def index(request):
    return render_to_response('saas/websitehomepage.html')

def register(request):

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
                service_list.append("Add Project")
            if e.addRequirements == True:
                service_list.append("Add Requirements")
            if e.modifyProjectStatus == True:
                service_list.append("Modify Project Status")
            if e.viewReqStatus== True:
                service_list.append("View Requirement Status")
            if e.viewProjectsManager == True:
                service_list.append("View Manager of Project")
            if e.modReqStatus == True:
                service_list.append("Modify Requirement Status")
            if e.viewAssignedReqs == True:
                service_list.append("View Assigned Requirements")

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

    context = RequestContext(request)
    current_user = request.user.username

    manager_list = Manager.objects.all()
    linklist = []

    for e in manager_list:
        user = e.user.username
        valid1 = e.tenant.addproject
        valid2 = e.tenant.addRequirements
        valid3 = e.tenant.modifyProjectStatus
        valid4 = e.tenant.viewReqStatus
        valid5 = e.tenant.viewProjectsManager
        if current_user == user:
            if valid1:
                linklist.append("addProject")
            if valid2:
                linklist.append("addRequirements")
            if valid3:
                linklist.append("modifyProjectStatus")
            if valid4:
                linklist.append("viewRequirement")
            if valid5:
                linklist.append("viewProjectManager")

    return render_to_response('saas/Dashboard.html',
                              {'linklist': linklist}, context)

def workerHome(request):
    context = RequestContext(request)

    current_user = request.user.username

    worker_list = Worker.objects.all()
    linklist = []


    for e in worker_list:
        user = e.user.username
        valid1 = e.tenant.viewAssignedReqs
        valid2 = e.tenant.modReqStatus
        if current_user == user:
            if valid1:
                linklist.append("viewAssignedRequirements")
            if valid2:
                linklist.append("modifyProjectStatus")

    #keeping just in case
    # for e in worker_list:
    #     user = e.user.username
    #     valid = e.tenant.viewAssignedReqs
    #     if current_user == user and valid == 1:
    #         for requirement in requirement_list:
    #             test = requirement.worker.user.username
    #             if current_user == test:
    #                 worker_requirements.append(requirement)

    return render_to_response('saas/workerHome.html',
                              {'linklist': linklist}, context)

def viewRequirements(request):

    context = RequestContext(request)
    worker_list = Worker.objects.all()
    current_user = request.user.username
    requirement_list = Requirement.objects.all()
    worker_requirements = []

    for e in worker_list:
        user = e.user.username
        valid = e.tenant.viewAssignedReqs
        if current_user == user and valid == 1:
            for requirement in requirement_list:
                test = requirement.worker.user.username
                if current_user == test:
                    worker_requirements.append("Description: " + requirement.description)
                    worker_requirements.append("Requirement Type: " + requirement.reqType)
                    worker_requirements.append("Time Required: " + str(requirement.timeReq))

    print worker_requirements

    return render_to_response('saas/viewAssignedRequirements.html',
                                {'worker_requirements': worker_requirements}, context)

def viewProjectsAddedByManager(request):
    context = RequestContext(request)

    project_list = Project.objects.all()
    current_user = request.user.username

    list = []

    for e in project_list:
        user = e.manager.user.username
        valid = e.tenant.viewProjectsManager
        if current_user == user and valid == 1:
            for project in project_list:
                test = project.manager.user.username
                if current_user == test:
                    list.append(project)

    return render_to_response('saas/viewManagerProjects.html',
                                {'list': list}, context)

def viewAllTenantProjects(request):
    context = RequestContext(request)

    project_list = Project.objects.all()
    current_user = request.user.username

    list = []

    for e in project_list:
        user = e.tenant.user.username
        if current_user == user:
            for project in project_list:
                test = project.tenant.user.username
                if current_user == test:
                    list.append(project)

    return render_to_response('saas/viewAllProjects.html',
                                {'list': list}, context)

def viewAllTenantRequirements(request):
    context = RequestContext(request)

    requirement_list = Requirement.objects.all()
    current_user = request.user.username

    list = []

    for e in requirement_list:
        user = e.tenant.user.username
        if current_user == user:
            list.append(e)

    return render_to_response('saas/viewAllReqTenant.html',
                                {'list': list}, context)
















