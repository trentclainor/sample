import React, { Component } from 'react';
import {Field, reduxForm} from 'redux-form'
import {Col, Form, Row} from "reactstrap";
import renderDateField from "../../../../utils/renderDateField";
import renderField from "../../../../utils/renderField";


class EducationForm extends Component {

  render() {
    return (
        <Form>
            <Field
              name='school'
              type="text"
              component={renderField}
              placeholder='Enter school name'
              label='School name'
            />
            <Field
              name='degree'
              type="text"
              component={renderField}
              placeholder='Enter degree'
              label='Degree'
            />
            <Row>
                <Col xs={6}>
                    <Field
                      name='start_date'
                      component={renderDateField}
                      placeholder='Enter start date'
                      label='From'
                      time={false}
                    />
                </Col>
                <Col xs={6}>
                    <Field
                      name='end_date'
                      component={renderDateField}
                      placeholder='Enter end date'
                      label='To'
                      time={false}
                    />
                </Col>
            </Row>
        </Form>
    );
  }
}


EducationForm = reduxForm({
  form: 'EducationForm', // a unique identifier for this form
})(EducationForm);

export default EducationForm
