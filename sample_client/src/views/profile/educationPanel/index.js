import {Alert, Button} from "reactstrap";

import React, {Component} from 'react';
import {connect} from 'react-redux';

import * as actionCreators from "../../../actions/profileEducation";
import {bindActionCreators} from "redux";

import EducationList from './partials/educationList';
import Icon from "../../../utils/icon";


class EducationPanel extends Component {

    componentDidMount() {
        if (this.props.userId && this.props.jobProfileId){
            this.props.actions.educationList(this.props.userId, this.props.jobProfileId);
        }
    }
    componentWillReceiveProps(nextProps) {
        if (this.props.jobProfileId !== nextProps.jobProfileId && nextProps.jobProfileId){
            nextProps.actions.educationList(nextProps.userId, nextProps.jobProfileId);
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
                Add some new education to get started.
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

    educationList = () => {
        return (
            <EducationList />
        )
    };

    educationPanel = () => {
        return (
            <div className="bg-white p-3 mb-3">
                <h4 className="border-bottom border-brand">
                    Education
                    <Button className='pull-right' size='sm' color='primary' onClick={() => this.props.actions.showEducationEditModal(null)}>
                        <Icon name='plus'/>
                    </Button>
                </h4>
                {this.props.loading && this.loadingMessage()}
                {this.props.educations.length === 0 && !this.props.loading && !this.props.errors.global && this.emptyMessage()}
                {this.props.errors.global && this.timeoutMessage()}
                {this.props.educations.length > 0 && this.educationList()}

            </div>
        )
    };

    render() {
        return (
            <div>
                {this.props.jobProfileId && this.educationPanel()}
            </div>
        )
    }
}

function mapStateToProps(state) {

    return {
        userId: state.auth.user.id,
        educations: state.profileEducation.educations,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
        loading: state.profileEducation.loading,
        errors: state.profileEducation.errors,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch),
    };
};

EducationPanel = connect(mapStateToProps, mapDispatchToProps)(EducationPanel);
export default EducationPanel;
