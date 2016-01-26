#!/usr/bin/env python3

import wsgiref.simple_server

from handywsgi import form
from handywsgi.form import textbox, email, textarea, button
from handywsgi.adapter import Adapter
from handywsgi.application import Application



def feedback_form(context):
    myform = form.Form(None, action=context.request.query.path, method=form.POST)
    username = textbox.LabeledTextbox(
            'Your name',
            None,
            name='username'
            )
    address = email.LabeledEmail(
            'Your email address',
            None,
            name='email-address'
            )
    myform.append(form.P(elements=[username, address]))
    myform.append(form.P(elements=[textarea.TextArea(None, name='feedback')]))
    myform.append(form.P(elements=[button.Submit('Hello button!', name=form.SUBMIT)]))
    return myform.__xml__


class FormApp(Application):

    def _on_request(self, context):
        print(feedback_form(context))
        self.add('form', feedback_form(context))

    def GET(self, context):
        self._on_request(context)

    def POST(self, context):
        self._on_request(context)
        self.content = repr(context.request.wsgi.post_data)


class config:
    default_template = 'form_demo'
    template_path = './examples'
    template_extension = 'html'


httpd = wsgiref.simple_server.make_server('', 8000, Adapter({'form_demo': FormApp(config())}))
print("Serving on port 8000...")

httpd.serve_forever()
