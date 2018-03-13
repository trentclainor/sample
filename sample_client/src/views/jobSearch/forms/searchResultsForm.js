import React, { Component } from 'react';
import {Field, reduxForm} from 'redux-form'
import {Button, Form, FormGroup, InputGroup, InputGroupAddon} from "reactstrap";
import Icon from "../../../utils/icon";
import {bindActionCreators} from "redux";
import * as dictHelpersActions from "../../../actions/dictHelpers";
import * as jobProfileActions from "../../../actions/jobProfile";
import {connect} from "react-redux";


class SearchForm extends Component {
    constructor(props) {
        super(props);
        this.state = props.initialValues;
    }

    componentDidMount() {
        this.props.jobProfileActions.jobProfileList();
    }

    searchTypes = [
        {value: "Standard", title: "Standard"},
        {value: "Personalised", title: "Personalised"},
    ];

    changeSelect = (event) => {
        this.setState({search_type: event.target.value})
    };

    render() {
        return (
            <Form onSubmit={this.props.handleSubmit}>
                <FormGroup>
                    {
                        this.state.search_type === 'Standard' ?
                            <InputGroup>
                                <Field
                                    className='form-control selector-variants selector-personalised'
                                    name='search_type'
                                    component='select'
                                    onChange={this.changeSelect}
                                >
                                    {this.searchTypes.map(item => (
                                        <option value={item.value} key={item.value}>
                                            {item.title}
                                        </option>
                                    ))}
                                </Field>
                                <Field
                                    className='form-control selector-variants selector-standard'
                                    name='name'
                                    type="text"
                                    component="input"
                                    placeholder='Job Title'
                                    required
                                />
                                <Field
                                    className='form-control selector-variants selector-standard'
                                    name='location'
                                    type="text"
                                    component="input"
                                    placeholder='Job Location'
                                />
                                <InputGroupAddon addonType='append'>
                                    <Button type="submit" color='brand'>
                                        <Icon name='search'/> Search
                                    </Button>
                                </InputGroupAddon>
                            </InputGroup>
                            :
                            <InputGroup>
                                <Field
                                    className='form-control selector-variants selector-personalised'
                                    name='search_type'
                                    component='select'
                                    onChange={this.changeSelect}
                                >
                                    {this.searchTypes.map(item => (
                                        <option value={item.value} key={item.value}>
                                            {item.title}
                                        </option>
                                    ))}
                                </Field>
                                <Field
                                    className='form-control selector-variants selector-personalised'
                                    name='job_profile_id'
                                    component='select'
                                    placeholder='Choose job profile'
                                    required
                                >
                                    <option value="">Choose job profile...</option>
                                    {this.props.jobProfiles.map(item => (
                                        <option value={item.id} key={item.id}>
                                            {item.name}
                                        </option>
                                    ))}
                                </Field>
                                <InputGroupAddon addonType='append'>
                                    <Button type="submit" color='brand'>
                                        <Icon name='search'/> Search
                                    </Button>
                                </InputGroupAddon>
                            </InputGroup>
                    }

                </FormGroup>
            </Form>
        );
    }
}

const mapStateToProps = (state) => ({
    jobProfiles: state.jobProfile.jobProfiles,
});

const mapDispatchToProps = (dispatch)  => ({
    dispatch,
    jobProfileActions: bindActionCreators(jobProfileActions, dispatch),
    dictHelpersActions: bindActionCreators(dictHelpersActions, dispatch),
});

SearchForm = connect(
    mapStateToProps,
    mapDispatchToProps
)(SearchForm);


SearchForm = reduxForm({
    form: 'SearchForm', // a unique identifier for this form
})(SearchForm);

export default SearchForm
