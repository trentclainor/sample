import {Alert, Button} from "reactstrap";

import React, { Component} from 'react';
import { connect } from 'react-redux';

import LanguageList from './partials/languageList';

import * as actionCreators from "../../../actions/profileLanguage";
import {bindActionCreators} from "redux";
import Icon from "../../../utils/icon";




class LanguagePanel extends Component {

    componentDidMount() {
        if (this.props.userId && this.props.jobProfileId){
            this.props.actions.languageList(this.props.userId, this.props.jobProfileId);
        }
    }
    componentWillReceiveProps(nextProps) {
        if (this.props.jobProfileId !== nextProps.jobProfileId && nextProps.jobProfileId){
            nextProps.actions.languageList(nextProps.userId, nextProps.jobProfileId);
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

    emptyMessage = () => {
        return (
            <Alert color="info">
                <h4>Nothing Found</h4>
                Add some new language to get started.
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

    languageList = () => {
        return (
            <LanguageList />
        )
    };

    languagePanel = () => {
        return (
            <div className="bg-white p-3 mb-3">
                <h4 className="border-bottom border-brand">
                    Language
                    <Button className='pull-right' size='sm' color='primary' onClick={() => this.props.actions.showLanguageEditModal(null)}>
                        <Icon name='plus'/>
                    </Button>
                </h4>
                {this.props.loading && this.loadingMessage()}
                {this.props.languages.length === 0 && !this.props.loading && !this.props.errors.global && this.emptyMessage()}
                {this.props.errors.global && this.timeoutMessage()}
                {this.props.languages.length > 0 && this.languageList()}

            </div>
        )
    };

    render() {
        return (
            <div>
                {this.props.jobProfileId && this.languagePanel()}
            </div>
        )
    }
}

function mapStateToProps(state) {

    return {
        userId: state.auth.user.id,
        languages: state.profileLanguage.languages,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
        loading: state.profileLanguage.loading,
        errors: state.profileLanguage.errors,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

LanguagePanel = connect(mapStateToProps, mapDispatchToProps)(LanguagePanel);
export default LanguagePanel;
