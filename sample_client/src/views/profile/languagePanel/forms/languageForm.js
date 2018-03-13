import React, { Component } from 'react';
import {Field, reduxForm} from 'redux-form'
import {Form} from "reactstrap";
import renderSelectField from "../../../../utils/renderSelectField";
import renderField from "../../../../utils/renderField";


class LanguageForm extends Component {

    //TODO get levels from server by api
    levels = [
        {value: 0, title: "Basic"},
        {value: 1, title: "Business"},
        {value: 2, title: "Fluent"}
    ];

    render() {
        return (
            <Form>
                <Field
                    name='name'
                    type="text"
                    component={renderField}
                    placeholder='Enter language name'
                    label='Language'
                />
                <Field
                    name='level'
                    data={this.levels}
                    valueField='value'
                    textField='title'
                    component={renderSelectField}
                    placeholder='Enter fluency'
                    label='Fluency'
                />
            </Form>
        );
    }
}


LanguageForm = reduxForm({
    form: 'LanguageForm', // a unique identifier for this form
})(LanguageForm);

export default LanguageForm
