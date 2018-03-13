import React, { Component } from 'react';
import {Field, reduxForm} from 'redux-form'
import {Form} from "reactstrap";
import renderMultipleCheckboxField from "../../../../utils/renderMultipleCheckboxField";
import renderSelectField from "../../../../utils/renderSelectField";
import {connect} from "react-redux";
import renderCheckboxField from "../../../../utils/renderCheckboxField";
import {bindActionCreators} from "redux";
import * as actionCreators from "../../../../actions/dictHelpers";
import CollapsibleCard from "../../../../utils/collapsibleCard";


class SearchPreferencesForm extends Component {

    render() {
        return (
            <Form>
                <h5>Looking For</h5>
                <Field
                    name='looking_for'
                    data={this.props.lookingForList}
                    valueField='value'
                    textField='title'
                    component={renderMultipleCheckboxField}
                />

                <h5>Preferred Location</h5>
                <Field
                    name='location'
                    data={this.props.locationList}
                    valueField='id'
                    textField='name'
                    component={renderSelectField}
                    placeholder='Enter Preferred Location'
                />

                <h5>Job Preferences</h5>
                <CollapsibleCard title='Industry' className='mb-4'>
                    <Field
                        name='industries'
                        data={this.props.industryList}
                        valueField='value'
                        textField='title'
                        component={renderMultipleCheckboxField}
                    />
                </CollapsibleCard>

                {/*<CollapsibleCard title='Role' className='mb-4'>*/}
                    {/*<Field*/}
                        {/*name='roles'*/}
                        {/*data={this.props.roleList}*/}
                        {/*valueField='value'*/}
                        {/*textField='title'*/}
                        {/*component={renderMultipleCheckboxField}*/}
                    {/*/>*/}
                {/*</CollapsibleCard>*/}

                <Field
                    name='weekly_email'
                    component={renderCheckboxField}
                    label='I would like to receive weekly emails with my relevant roles.'
                />
            </Form>
        );
    }
}


const mapStateToProps = (state) => ({
    lookingForList: state.dictHelpers.lookingForList,
    locationList: state.dictHelpers.locationList,
    industryList: state.dictHelpers.industryList,
    roleList: state.dictHelpers.roleList,
    userId: state.auth.user.id,
    jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
});

const mapDispatchToProps = (dispatch)  => ({
    dispatch,
    actions: bindActionCreators(actionCreators, dispatch),
});

SearchPreferencesForm = connect(
    mapStateToProps,
    mapDispatchToProps
)(SearchPreferencesForm);


SearchPreferencesForm = reduxForm({
    form: 'SearchPreferencesForm', // a unique identifier for this form
})(SearchPreferencesForm);

export default SearchPreferencesForm
