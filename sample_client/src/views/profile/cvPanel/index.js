import {Alert, Button} from "reactstrap";

import React, { Component} from 'react';
import { connect } from 'react-redux';

import CVList from './partials/cvList';

import * as actionCreators from "../../../actions/jobProfile";
import {bindActionCreators} from "redux";
import Icon from "../../../utils/icon";



class CVPanel extends Component {

    componentDidMount() {
        this.props.actions.jobProfileList();
    }
    componentWillUnmount() {
        this.props.actions.selectJobProfile({})
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
                Add some new CV to get started.
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

    infoMessage = () => {
        return (
            <div>
                {this.props.selectedJobProfile ?
                    <p>
                    <small className="text-muted">
                        You will be able to upload upto 3 CV's and set one as default job profile to match jobs for you.
                    </small>
                    </p>
                    :
                    <Alert color='info'>
                        To get more information click on any row.
                    </Alert>
                }
            </div>
        )
    };

    cvList = () => {
        return (
            <CVList />
        )
    };

    render() {
        return (
            <div className="bg-white p-3 mb-3">
                <h4 className="border-bottom border-brand">
                    Upload CV
                    <Button className='pull-right' size='sm' color='primary' onClick={() => this.props.actions.showJobProfileEditModal(null)}>
                        <Icon name='plus'/>
                    </Button>
                </h4>
                {this.props.loading && this.loadingMessage()}
                {this.props.jobProfiles.length === 0 && !this.props.loading && !this.props.errors.global && this.emptyMessage()}
                {this.props.errors.global && this.timeoutMessage()}
                {this.props.jobProfiles.length > 0 && this.infoMessage()}
                {this.props.jobProfiles.length > 0 && this.cvList()}

            </div>
        )
    }
}

function mapStateToProps(state) {

    return {
        jobProfiles: state.jobProfile.jobProfiles,
        // selectedJobProfile: state.jobProfile.selectedJobProfile,
        selectedJobProfile : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
        loading: state.jobProfile.loading,
        errors: state.jobProfile.errors,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

CVPanel = connect(mapStateToProps, mapDispatchToProps)(CVPanel);
export default CVPanel;
