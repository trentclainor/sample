import React, { Component } from 'react';
import {Field, reduxForm} from 'redux-form'
import {Form} from "reactstrap";
import renderField from "../../../../utils/renderField";
import renderFileField from "../../../../utils/renderFileField";


class CVForm extends Component {

  render() {
    return (
        <Form onSubmit={this.props.handleSubmit}>
            <Field
              name='name'
              type="text"
              component={renderField}
              placeholder='Enter name'
              label='Name'
            />
            <Field
              name='cv'
              type="file"
              component={renderFileField}
              buttonText='CV'
              label='CV file'
            />
        </Form>
    );
  }
}


CVForm = reduxForm({
  form: 'CVForm', // a unique identifier for this form
})(CVForm);

export default CVForm
