import React, { Component } from 'react';
import {Field, reduxForm} from 'redux-form'
import { Form } from "reactstrap";
import renderField from "../../../../utils/renderField";
import renderFileField from "../../../../utils/renderFileField";


class BasicInfoForm extends Component {

  render() {
    return (
        <Form horizontal>
            <Field
              name='name'
              type="text"
              component={renderField}
              placeholder='Enter name'
              label='Name'
            />
            <Field
              name='photo'
              type="file"
              component={renderFileField}
              buttonText='Photo'
              label='Photo'
            />
            <Field
              name='email'
              type="email"
              component={renderField}
              placeholder='Enter email'
              label='Email'
            />
            <Field
              name='phone'
              type="text"
              component={renderField}
              placeholder='Enter phone'
              label='Phone'
            />
            <Field
              name='linkedin'
              type="text"
              component={renderField}
              placeholder='Enter linkedin profile URL'
              label='Linkedin Profile URL'
            />
            <Field
              name='address1'
              type="text"
              component={renderField}
              placeholder=''
              label='Address'
            />
            <Field
              name='address2'
              type="text"
              component={renderField}
            />
            <Field
              name='address3'
              type="text"
              component={renderField}
            />
        </Form>
    );
  }
}


BasicInfoForm = reduxForm({
  form: 'BasicInfoForm', // a unique identifier for this form
})(BasicInfoForm);

export default BasicInfoForm
