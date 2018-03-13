import React from 'react'
import {Col, Label, Input, FormGroup, FormText, Row} from "reactstrap";

const renderFileField = ({input, label, type, buttonText, placeholder, meta: {touched, error, warning}, ...rest}) => {
    let val = input.value;
    delete input.value;

    const getValidationState = () => {
        return error ? 'danger' : warning ? 'warning' : null;
    };

    let getBorderColor = () => {
      let state = getValidationState();
      return state ? 'border-' + state: ''
    };

    const onCustomChange = (e) => {
        input.onChange(e.target.files[0])
    };

    return <FormGroup>
        {label ?
            <Label>{label}</Label>
            :
            ''
        }
        <Row>
            <Col xs='12'>
                    <span className={"btn btn-default btn-outline-secondary btn-file " + getBorderColor()}>
                        {val ?
                            <span>Change {buttonText}</span>
                            :
                            <span>Upload {buttonText}</span>
                        }

                        <Input
                            state={getValidationState()}
                            onChange={onCustomChange}
                            type='file'
                        />
                    </span>
                {touched &&
                ((error && <FormText color="danger">{error}</FormText>) ||
                    (warning && <FormText color="warning">{warning}</FormText>))}
            </Col>
        </Row>
    </FormGroup>
}


export default renderFileField
