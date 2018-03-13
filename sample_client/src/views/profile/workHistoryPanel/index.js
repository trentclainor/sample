import {Alert, Button} from "reactstrap";

import React, { Component} from 'react';
import { connect } from 'react-redux';

import WorkHistoryList from './partials/workHistoryList';

import * as actionCreators from "../../../actions/profileWorkHistory";
import {bindActionCreators} from "redux";
import Icon from "../../../utils/icon";




class WorkHistoryPanel extends Component {

    componentDidMount() {
        if (this.props.userId && this.props.jobProfileId){
            this.props.actions.workHistoryList(this.props.userId, this.props.jobProfileId);
        }
    }
    componentWillReceiveProps(nextProps) {
        if (this.props.jobProfileId !== nextProps.jobProfileId && nextProps.jobProfileId){
            nextProps.actions.workHistoryList(nextProps.userId, nextProps.jobProfileId);
        }
    }

    loadingMessage = () => {
        return (
            <Alert color='info'>
                <h4>Just one second</h4>
                We are fetching that content for you.
            </Alert>
        )
    };

    emptyMessage = () => {
        return (
            <Alert color='info'>
                <h4>Nothing Found</h4>
                Add some new work history to get started.
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

    workHistoryList = () => {
        return (
            <WorkHistoryList />
        )
    };

    workHistoryPanel = () => {
        return (
            <div className="bg-white p-3 mb-3">
                <h4 className="border-bottom border-brand">
                    Work History
                    <Button className='pull-right' size='sm' color='primary' onClick={() => this.props.actions.showWorkHistoryEditModal(null)}>
                        <Icon name='plus'/>
                    </Button>
                </h4>
                {this.props.loading && this.loadingMessage()}
                {this.props.workHistories.length === 0 && !this.props.loading && !this.props.errors.global && this.emptyMessage()}
                {this.props.errors.global && this.timeoutMessage()}
                {this.props.workHistories.length > 0 && this.workHistoryList()}

            </div>
        )
    };

    render() {
        return (
            <div>
                {this.props.jobProfileId && this.workHistoryPanel()}
            </div>
        )
    }
}

function mapStateToProps(state) {

    return {
        userId: state.auth.user.id,
        workHistories: state.profileWorkHistory.workHistories,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
        loading: state.profileWorkHistory.loading,
        errors: state.profileWorkHistory.errors,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

WorkHistoryPanel = connect(mapStateToProps, mapDispatchToProps)(WorkHistoryPanel);
export default WorkHistoryPanel;
