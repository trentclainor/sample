import React from 'react'
import {Label, FormGroup, FormText} from "reactstrap";
import DropdownList from 'react-widgets/lib/DropdownList';

const renderSelectField = ({input, data, valueField, label, meta: {touched, error, warning}, ...rest}) => {

    const getValidationState = () => {
        return error ? 'danger' : warning ? 'warning' : null;
    };

    let getBorderColor = () => {
      let state = getValidationState();
      return state ? 'border-' + state: ''
    };

    let handleChange = function(item) {
        let value = item;

        if (valueField) {
            value = item[valueField]
        }

        input.onChange(value)
    };

    let getvalue = function() {
        let value = input.value;

        if (valueField) {
            let values = data.filter(item => item[valueField] === input.value);
            value = values ? values[0] : -1;
        }

        return value;
    };

    return <FormGroup>
        {label ?
            <Label>{label}</Label>
            :
            ''
        }
        <DropdownList
            containerClassName={getBorderColor()}
            {...rest}
            {...input}
            data={data}
            value={getvalue()}
            onChange={handleChange}
        />

        {touched &&
        ((error && <FormText color="danger">{error}</FormText>) ||
            (warning && <FormText color="warning">{warning}</FormText>))}
    </FormGroup>
};


export default renderSelectField
