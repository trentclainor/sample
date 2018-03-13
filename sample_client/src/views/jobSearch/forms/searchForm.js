import React, { Component } from 'react';
import {Field, reduxForm} from 'redux-form'
import {Button, Form, FormGroup, InputGroup, InputGroupAddon} from "reactstrap";
import Icon from "../../../utils/icon";
import {bindActionCreators} from "redux";
import * as jobProfileActions from "../../../actions/jobProfile";
import * as dictHelpersActions from "../../../actions/dictHelpers";
import {connect} from "react-redux";


class SearchForm extends Component {
    constructor(props) {
        super(props);
        this.state = props.initialValues;
    }

    componentDidMount() {
        this.props.jobProfileActions.jobProfileList();
    }

    changeSelect = (value) => {
        this.setState({search_type: value});
        this.props.change('search_type', value);
    };

    render() {
        return (
            <Form className='bg-white-25 p-1 p-md-5 rounded' onSubmit={this.props.handleSubmit}>
                <Field
                    className='form-control selector-variants selector-standard hidden'
                    name='search_type'
                    type="text"
                    component="input"
                    value={this.state.search_type}
                />
                <FormGroup className='mb-3 mb-md-5 text-center'>
                    <div className="btn-group btn-group-switcher rounded-more" role="group" id="searchSwitch">
                        <Button color='light' className={this.state.search_type === 'Standard' ? 'active' : null} onClick={() => this.changeSelect('Standard')}>
                            Standard <Icon name='info-circle'/>
                        </Button>
                        <Button color='light' className={this.state.search_type === 'Personalised' ? 'active' : null} onClick={() => this.changeSelect('Personalised')}>
                            Personalised <Icon name='info-circle'/>
                        </Button>
                    </div>
                </FormGroup>
                {
                    this.state.search_type === 'Standard' ?
                        <FormGroup className='group-switcher-item active mb-0'>
                            <p className="text-white text-center"><small>Get Standard Search Results based on the fields below</small></p>
                            <InputGroup>
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
                                <InputGroupAddon addonType="append">
                                    <Button color='brand'>
                                        <Icon name='search'/> Search
                                    </Button>
                                </InputGroupAddon>
                            </InputGroup>
                        </FormGroup>
                        :
                        <FormGroup className='group-switcher-item active mb-0'>
                            <p className="text-white text-center"><small>Get Personalised Search Results based on the CV you've uploaded</small></p>
                            <InputGroup>
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
                                <InputGroupAddon addonType="append">
                                    <Button color='brand'>
                                        <Icon name='search'/> Search
                                    </Button>
                                </InputGroupAddon>
                            </InputGroup>
                        </FormGroup>
                }

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
