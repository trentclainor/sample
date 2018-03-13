import React, { Component } from 'react';
import {Field, reduxForm} from 'redux-form'
import {Col, Form, Row} from "reactstrap";
import renderDateField from "../../../../utils/renderDateField";
import renderField from "../../../../utils/renderField";


class WorkHistoryForm extends Component {

    render() {
        return (
            <Form>
                <Field
                    name='company_name'
                    type="text"
                    component={renderField}
                    placeholder='Enter company name'
                    label='Company name'
                />
                <Field
                    name='role'
                    type="text"
                    component={renderField}
                    placeholder='Enter role'
                    label='Role'
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


WorkHistoryForm = reduxForm({
    form: 'WorkHistoryForm', // a unique identifier for this form
})(WorkHistoryForm);

export default WorkHistoryForm
