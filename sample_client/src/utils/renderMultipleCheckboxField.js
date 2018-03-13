import React from 'react'
import {Label, FormGroup, FormText, Input} from "reactstrap";


const renderMultipleCheckboxField = ({input, data, valueField, textField, label, meta: {touched, error, warning}, ...rest}) => {

    const {name, onChange, onBlur, onFocus} = input;
    const inputValue = input.value;

    const checkboxes = data.map((item, index) => {

        let value = valueField ? item[valueField] : item['value'];
        let cbLabel = textField ? item[textField] : item['label'];
        let checked = inputValue.includes(value);

        let changeArray = (checked, value) => {
            const arr = [...inputValue];

            if (checked) {
                arr.push(value);
            }
            else {
                arr.splice(arr.indexOf(value), 1);
            }
            onBlur(arr);
            return onChange(arr);
        };


        const handleChange = (event) => {
            return changeArray(event.target.checked, value);
        };



        return (
            <div key={`checkbox-${index}`} className="custom-control custom-checkbox" onClick={() => changeArray(!checked, value)}>
                <Input
                    type="checkbox"
                    name={`${name}[${index}]`}
                    value={value}
                    checked={checked}
                    onChange={handleChange}
                    onFocus={onFocus}
                    className="custom-control-input"/>
                <label className="custom-control-label">
                    {cbLabel}
                </label>
            </div>
        );
    });

    const getValidationState = () => {
        return error ? 'danger' : warning ? 'warning' : null;
    };

    return <FormGroup>

        {label ?
            <div>
                <Label>{label}</Label>
                <br/>
            </div>
            :
            ''
        }

        {checkboxes}

        {touched &&
        ((error && <FormText color="danger">{error}</FormText>) ||
            (warning && <FormText color="warning">{warning}</FormText>))}
    </FormGroup>
};


export default renderMultipleCheckboxField
