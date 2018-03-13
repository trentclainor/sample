import React from 'react'
import {FormGroup, FormText, Input, Label} from "reactstrap";

const renderCheckboxField = ({input, label, meta: {touched, error, warning}, ...rest}) => {

    const getValidationState = () => {
        return error ? 'danger' : warning ? 'warning' : null;
    };

    let changeValue = () => {
        input.onChange(!input.value);
    };

    return <FormGroup>
        <div className="custom-control custom-checkbox" onClick={changeValue}>
            <Input
                state={getValidationState()}
                type="checkbox"
                {...input}
                {...rest}
                className="custom-control-input"
                checked={input.value}/>
            <label
                className="custom-control-label"
            >
                {label}
            </label>
        </div>

        {touched &&
        ((error && <FormText color="danger">{error}</FormText>) ||
            (warning && <FormText color="warning">{warning}</FormText>))}
    </FormGroup>
}


export default renderCheckboxField
