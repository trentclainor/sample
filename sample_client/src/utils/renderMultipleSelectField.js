import React from 'react'
import {Label, FormGroup, FormText, Input} from "reactstrap";
import Select from 'react-select'

const renderMultiselect = ({input, data, textField, valueField, filter, label, defaultValue, placeholder, name, meta: {touched, error, warning}, ...rest}) => {

    const getValidationState = () => {
        return error ? 'danger' : warning ? 'warning' : null;
    };

    let getBorderColor = () => {
        let state = getValidationState();
        return state ? 'border-' + state: ''
    };

    let handleChange = function(inputValue) {
        let value = inputValue;

        if (valueField) {
            value = value.map(item => item[valueField])
        }

        input.onChange(value);
    };

    return <FormGroup>
        {label ?
            <Label>{label}</Label>
            :
            ''
        }
        <Select {...input}
                multi
                onBlur={() => input.onBlur()}
                value={input.value || []} // requires value to be an array
                options={data}
                valueKey={valueField}
                labelKey={textField}
                closeOnSelect={false}
                onChange={handleChange}
        />

        {touched &&
        ((error && <FormText color="danger">{error}</FormText>) ||
            (warning && <FormText color="warning">{warning}</FormText>))}
    </FormGroup>
};

export default renderMultiselect
