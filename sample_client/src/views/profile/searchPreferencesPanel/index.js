import {Alert, Button} from "reactstrap";

import React, { Component} from 'react';
import { connect } from 'react-redux';

import * as actionCreators from "../../../actions/profileSearchPreference";
import * as dictHelpersActions from "../../../actions/dictHelpers";
import {bindActionCreators} from "redux";
import SearchPreferencesForm from "./forms/preferenceForm";
import {SubmissionError, submit} from "redux-form";
import Icon from "../../../utils/icon";




class SearchPreferencesPanel extends Component {
    constructor() {
        super();
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(values){
        let action = null;
        if ('id' in values) {
            action = this.props.actions.preferenceUpdate(this.props.userId, this.props.jobProfileId, values);
        } else {
            action = this.props.actions.preferenceCreate(this.props.userId, this.props.jobProfileId, values);
        }
        return action
            .catch(error => {
                throw new SubmissionError(error.response.data)
            })
    }

    componentDidMount() {
        this.props.dictHelpersActions.lookingForList();
        this.props.dictHelpersActions.locationList();
        this.props.dictHelpersActions.industryList();
        // this.props.actions.roleList();
        if (this.props.userId && this.props.jobProfileId){

            this.props.actions.preferenceList(this.props.userId, this.props.jobProfileId);
        }
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.jobProfileId !== nextProps.jobProfileId && nextProps.jobProfileId){
            nextProps.actions.preferenceList(nextProps.userId, nextProps.jobProfileId);
        }
    }

    loadingMessage = () => {
        return (
            <Alert color="info">
                <h4>Just one second</h4>
                We are fetching that content for you.
            </Alert>
        )
    };

    chooseCVMessage = () => {
        return (
            <Alert color="info">
                To load preferences choose any CV.
            </Alert>
        )
    };

    timeoutMessage  = () => {
        return (
            <Alert color="danger">
                <h4>{this.props.errors.global}</h4>
                Temporal error. Try again later.
            </Alert>
        )
    };

    getForm  = (initialValues) => {
        if (initialValues){
            return (
                <SearchPreferencesForm
                    onSubmit={this.handleSubmit}
                    initialValues={initialValues}
                    enableReinitialize={true}
                />
            )
        }
        return (
            <SearchPreferencesForm
                onSubmit={this.handleSubmit}
                enableReinitialize={true}
            />
        )
    };


    preferenceForm = () => {
        return this.props.preferences.map(preference => {
            return (
                <div key={preference.id}>
                    {this.getForm(preference)}
                </div>
            )
        })
    };

    preferencePanel = () => {
        return (
            <div className="filter-panel border border-gray p-3">
                <h4 className="border-bottom border-brand">
                    <Icon name="sliders"/> {' '}
                    Search Preferences
                </h4>
                {!this.props.jobProfileId && this.chooseCVMessage()}
                {this.props.jobProfileId && this.props.loading && this.loadingMessage()}
                {this.props.jobProfileId && this.props.errors.global && this.timeoutMessage()}
                {this.props.jobProfileId && this.props.preferences.length === 0 && !this.props.loading && !this.props.errors.global && this.getForm()}
                {this.props.jobProfileId && this.props.preferences.length > 0 && this.preferenceForm()}

                {this.props.jobProfileId && !this.props.loading && !this.props.errors.global ?
                    <div className="text-right">
                        <hr/>
                        <Button color='success' onClick={() => this.props.submitAction('SearchPreferencesForm')}>Save Preferences</Button>
                    </div>
                    :
                    ""
                }

            </div>
        )
    };

    render() {
        return (
            <div>
                {this.preferencePanel()}
            </div>
        )
    }
}

function mapStateToProps(state) {

    return {
        userId: state.auth.user.id,
        preferences: state.profilePreference.preferences,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
        loading: state.profileLanguage.loading,
        errors: state.profileLanguage.errors,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch),
        dictHelpersActions: bindActionCreators(dictHelpersActions, dispatch),
        submitAction: bindActionCreators(submit, dispatch)
    };
};

SearchPreferencesPanel = connect(mapStateToProps, mapDispatchToProps)(SearchPreferencesPanel);
export default SearchPreferencesPanel;
