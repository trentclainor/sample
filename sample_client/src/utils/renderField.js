import React from 'react'
import {Label, Input, FormGroup, FormText} from "reactstrap";

const renderField = ({input, label, type, placeholder, meta: {touched, error, warning}, ...rest}) => {

    const getValidationState = () => {
        return error ? 'danger' : warning ? 'warning' : null;
    };

    return <FormGroup>
        {label ?
            <Label>{label}</Label>
            :
            ''
        }
        <Input
            {...input}
            {...rest}
            state={getValidationState()}
            type={type}
            placeholder={placeholder}
        />

        {touched &&
        ((error && <FormText color="danger">{error}</FormText>) ||
            (warning && <FormText color="warning">{warning}</FormText>))}
    </FormGroup>
}


export default renderField
