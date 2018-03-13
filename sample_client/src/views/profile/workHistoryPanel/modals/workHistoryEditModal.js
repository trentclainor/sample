import {Button, Modal, ModalBody, ModalFooter} from "reactstrap";

import React, { Component } from 'react';

import {connect} from "react-redux";

import WorkHistoryForm from "../forms/workHistoryForm";
import {SubmissionError, submit} from 'redux-form'

import moment from "moment";

import * as actionCreators from "../../../../actions/profileWorkHistory";
import {bindActionCreators} from "redux";




class WorkHistoryEditModal extends Component {
    constructor() {
        super();
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(values){
        let _this = this;
        let action = null;
        let _values = Object.assign({}, values);
        if ('start_date' in _values && _values.start_date){
            _values.start_date = moment(_values.start_date).format('YYYY-MM-DD')
        }
        if ('end_date' in _values && _values.end_date){
            _values.end_date = moment(_values.end_date).format('YYYY-MM-DD')
        }
        if ('id' in _values) {
            action = this.props.actions.workHistoryUpdate(this.props.userId, this.props.jobProfileId, _values);
        } else {
            action = this.props.actions.workHistoryCreate(this.props.userId, this.props.jobProfileId, _values);
        }
        return action
            .then(function (response) {
                _this.props.actions.hideWorkHistoryEditModal();
            })
            .catch(error => {
                throw new SubmissionError(error.response.data)
            })
    }

    render() {
        return (
            <Modal isOpen={this.props.isShownWorkHistoryEditModal} toggle={this.props.actions.hideWorkHistoryEditModal}>
                <div className="modal-header bg-brand-gradient">
                    <h5 className="modal-title text-white" id="basicInfoModalTitle">Work History</h5>
                    <button type="button" className="close text-white" onClick={this.props.actions.hideWorkHistoryEditModal} aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <ModalBody>
                    {this.props.initialValues ?
                        <WorkHistoryForm
                            onSubmit={this.handleSubmit}
                            initialValues={this.props.initialValues}
                            enableReinitialize={true}/>
                        :
                        <WorkHistoryForm
                            onSubmit={this.handleSubmit}
                            enableReinitialize={true}/>
                    }
                </ModalBody>
                <ModalFooter>
                    <Button color='outline-secondary' onClick={this.props.actions.hideWorkHistoryEditModal}>Close</Button>
                    <Button color='brand' onClick={() => this.props.submitAction('WorkHistoryForm')}>Save</Button>
                </ModalFooter>
            </Modal>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        initialValues: state.profileWorkHistory.workHistory ? state.profileWorkHistory.workHistory: null,
        userId: state.auth.user.id,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
        selectedJobProfile: state.jobProfile.selectedJobProfile,
        isShownWorkHistoryEditModal: state.profileWorkHistory.isShownWorkHistoryEditModal
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch),
        submitAction: bindActionCreators(submit, dispatch)
    };
};

WorkHistoryEditModal = connect(mapStateToProps, mapDispatchToProps)(WorkHistoryEditModal);
export default WorkHistoryEditModal;
