from .models import User

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

from pyramid.httpexceptions import (
    HTTPFound,
    )


@view_config(route_name='home', renderer='templates/home.jinja2', permission='view')
def home_view(request):
    userid = authenticated_userid(request)
    return dict(userid=userid)

@forbidden_view_config(renderer='templates/login.jinja2')
def forbidden_view(request):
    return HTTPFound(location=request.route_url('login'))

@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    name = ''
    password = ''
    message = ''
    if 'form.submitted' in request.params:
        name = request.params['username']
        password = request.params['password']
        user = User.find_by_name(name)
        if user.verify_password(password):
            headers = remember(request, user.name)
            return HTTPFound(location=request.route_url('home'), headers=headers)

        message = 'Login Failed'

    return dict(name=name, password=password, message=message, url=request.application_url + '/login')


@view_config(route_name='logout', renderer='templates/logout.jinja2')
def logout_view(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)

@view_config(route_name='sign_up', renderer='templates/sign_up.jinja2')
def sign_up_view(request):
    message = ''

    if 'form.submitted' in request.params:
        name = request.params['username']
        password = request.params['password']
        if User.find_by_name(name) is None:
            User.add_user(name, password)
            return HTTPFound(location=request.route_url('login'))

        message = 'User is already exist'

    return dict(message=message)
