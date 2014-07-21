"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, \
    session

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import ExampleForm
from models import ExampleModel


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        if request.form['username']:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('social'))
        else:
            error = 'You must enter your name'
    return render_template('home.html', error=error)

#*******************PAGES**************************

#Social page 1st
@app.route('/social/', methods=['GET', 'POST'])
@login_required
def social():
    return render_template('social.html')

#Enterprise page 2nd
@app.route('/enterprising/')
@login_required
def enterprising():
    return render_template('enterprising.html')

#Conventional page 3rd
@app.route('/conventional/')
@login_required
def conventional():
    return render_template('conventional.html')

#Realistic page 4th
@app.route('/realistic/')
@login_required
def realistic():
    return render_template('realistic.html')

#Investigative 5th
@app.route('/investigative/')
@login_required
def investigative():
    return render_template('investigative.html')

#Artistic 6th page
@app.route('/artistic/')
@login_required
def artistic():
    return render_template('artistic.html')

#**************************************************

#*********************** ADD ATTRIBUTES TO SESSION*****************
#Social page 1st
@app.route('/add_social/', methods=['GET', 'POST'])
@login_required
def add_social():
    social_list = request.form.getlist('social_attr')
    i = 0
    for s in social_list:
        i += 1
    session['social'] = i
    return redirect(url_for('enterprising'))

#Enterprise page 2nd
@app.route('/add_enterprise/', methods=['GET', 'POST'])
@login_required
def add_enterprise():
    enterprise_list = request.form.getlist('enterprise_attr')
    i = 0
    for e in enterprise_list:
        i += 1
    session['enterprise'] = i
    return redirect(url_for('conventional'))

#Conventional page 3rd
@app.route('/add_conventional/', methods=['GET', 'POST'])
@login_required
def add_conventional():
    conventional_list = request.form.getlist('conventional_attr')
    i = 0
    for c in conventional_list:
        i += 1
    session['conventional'] = i
    return redirect(url_for('realistic'))

#4th page
@app.route('/add_realistic/', methods=['GET', 'POST'])
@login_required
def add_realistic():
    realistic_list = request.form.getlist('realistic_attr')
    i = 0
    for r in realistic_list:
        i += 1
    session['realistic'] = i
    return redirect(url_for('investigative'))

#5th page
@app.route('/add_investigative/', methods=['GET', 'POST'])
@login_required
def add_investigative():
    investigative_list = request.form.getlist('investigative_attr')
    i = 0
    for v in investigative_list:
        i += 1
    session['investigative'] = i
    return redirect(url_for('artistic'))

#artistic 6th page
@app.route('/add_artistic/', methods=['GET', 'POST'])
@login_required
def add_artistic():
    artistic_list = request.form.getlist('artistic_attr')
    i = 0
    for a in artistic_list:
        i += 1
    session['artistic'] = i
    return redirect(url_for('results'))

#****************************************************************

##RESULTS returns the totals from each page, and gets
#the 3 highest
@app.route('/results/', methods=['GET', 'POST'])
@login_required
def results():
    name = session['username']
    soc = session['social']
    enter = session['enterprise']
    con = session['conventional']
    real = session['realistic']
    inv = session['investigative']
    art = session['artistic']

    attr_tuples = [
        ('Social', soc, 'Social occupations frequently involve working with, '
                        'communicating with, and teaching people. These '
                        'occupations often involve helping or providing service to others.'),
        ('Enterprising', enter, 'Enterprising occupations frequently involve starting up and '
                                'carrying out projects. These occupations can involve leading people'
                                ' and making many decisions.Sometimes they require risk taking '
                                'and often deal with business.'),
        ('Conventional', con, 'Conventional occupations frequently involve following set '
                              'procedures and routines. These occupations can include working '
                              'with data and details more than with ideas. Usually there is a '
                              'clear line of authority to follow.'),
        ('Realistic', real, 'Realistic occupations frequently involve work activities that '
                            'include practical, hands-on problems and solutions. They often '
                            'deal with plants, animals, and real-world materials like wood, '
                            'tools, and machinery. Many of the occupations require working '
                            'outside, and do not involve a lot of paperwork or working '
                            'closely with others.'),
        ('Investigative', inv, 'Investigative occupations frequently involve working with '
                               'ideas, and require an extensive amount of thinking. These '
                               'occupations can involve searching for facts and figuring out'
                               ' problems mentally.'),
        ('Artistic', art, 'Artistic occupations frequently involve working with forms, '
                          'designs and patterns. They often require self-expression and '
                          'the work can be done without following a clear set of rules.')
    ]
    attr_tuples = sorted(attr_tuples, key=lambda attr: attr[1], reverse=True)
    first = attr_tuples[0][0]
    second = attr_tuples[1][0]
    third = attr_tuples[2][0]

    first_descr = attr_tuples[0][2]
    second_descr = attr_tuples[1][2]
    third_descr = attr_tuples[2][2]

    if attr_tuples[2][1] == attr_tuples[3][1]:
        third = "(tie) " + attr_tuples[2][0] + "/" + attr_tuples[3][0]

    return render_template('results.html', name=name, soc=soc, enter=enter, \
                           con=con, real=real, inv=inv, art=art, first=first, second=second, \
                           third=third, first_descr=first_descr, second_descr=second_descr, \
                           third_descr=third_descr)




#def say_hello(username):
#    Contrived example to demonstrate Flask's url routing capabilities
#    return 'Hello %s' % username

"""
@login_required
def list_examples():
    #List all examples
    examples = ExampleModel.query()
    form = ExampleForm()
    if form.validate_on_submit():
        example = ExampleModel(
            example_name=form.example_name.data,
            example_description=form.example_description.data,
            added_by=users.get_current_user()
        )
        try:
            example.put()
            example_id = example.key.id()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_examples'))
    return render_template('list_examples.html', examples=examples, form=form)
"""

"""
@login_required
def edit_example(example_id):
    example = ExampleModel.get_by_id(example_id)
    form = ExampleForm(obj=example)
    if request.method == "POST":
        if form.validate_on_submit():
            example.example_name = form.data.get('example_name')
            example.example_description = form.data.get('example_description')
            example.put()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
    return render_template('edit_example.html', example=example, form=form)
"""


"""
@login_required
def delete_example(example_id):
    #Delete an example object
    example = ExampleModel.get_by_id(example_id)
    try:
        example.key.delete()
        flash(u'Example %s successfully deleted.' % example_id, 'success')
        return redirect(url_for('list_examples'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('list_examples'))
"""

@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


@cache.cached(timeout=60)
def cached_examples():
    """This view should be cached for 60 sec"""
    examples = ExampleModel.query()
    return render_template('list_examples_cached.html', examples=examples)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

