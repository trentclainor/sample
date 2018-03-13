import React from 'react'
import {Label, FormGroup, FormText} from "reactstrap";
import DateTimePicker from 'react-widgets/lib/DateTimePicker';
import moment from "moment/moment";
import momentLocalizer from 'react-widgets-moment';

momentLocalizer();

const renderDateField = ({input: {value, name, onChange}, label, afterChange, meta: {touched, error, warning}, ...rest}) => {

    const getValidationState = () => {
        return error ? 'danger' : warning ? 'warning' : null;
    };

    let onChangeCustom = onChange;
    if (afterChange) {
        onChangeCustom = function(...args) {
            onChangeCustom(...args);
            afterChange(...args);
        }
    }

    return <FormGroup>
        {label ?
            <Label>{label}</Label>
            :
            ''
        }
        <DateTimePicker
            {...rest}
            format="YYYY-MM-DD"
            name={name}
            onChange={onChangeCustom}
            time={false}
            value={value ? moment(value).toDate() : null}
        />

        {touched &&
        ((error && <FormText color="danger">{error}</FormText>) ||
            (warning && <FormText color="warning">{warning}</FormText>))}
    </FormGroup>
};


export default renderDateField
