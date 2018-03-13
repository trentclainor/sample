import {Button, Modal, ModalBody, ModalFooter} from "reactstrap";

import React, { Component } from 'react';
import {connect} from "react-redux";

import {SubmissionError, submit} from 'redux-form'
import moment from "moment";

import * as actionCreators from "../../../../actions/profileEducation";
import {bindActionCreators} from "redux";

import EducationForm from "../forms/educationForm";



class EducationEditModal extends Component {
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
            action = this.props.actions.educationUpdate(this.props.userId, this.props.jobProfileId, _values);
        } else {
            action = this.props.actions.educationCreate(this.props.userId, this.props.jobProfileId, _values);
        }
        return action
            .then(function (response) {
                _this.props.actions.hideEducationEditModal();
            })
            .catch(error => {
                throw new SubmissionError(error.response.data)
            })
    }

    render() {
        return (
            <Modal isOpen={this.props.isShownEducationEditModal} toggle={this.props.actions.hideEducationEditModal}>
                <div className="modal-header bg-brand-gradient">
                    <h5 className="modal-title text-white" id="basicInfoModalTitle">Education</h5>
                    <button type="button" className="close text-white" onClick={this.props.actions.hideEducationEditModal} aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <ModalBody>
                    {this.props.initialValues ?
                        <EducationForm
                            onSubmit={this.handleSubmit}
                            initialValues={this.props.initialValues}
                            enableReinitialize={true}/>
                        :
                        <EducationForm
                            onSubmit={this.handleSubmit}
                            enableReinitialize={true}/>
                    }
                </ModalBody>
                <ModalFooter>
                    <Button color='outline-secondary' onClick={this.props.actions.hideEducationEditModal}>Close</Button>
                    <Button color='brand' onClick={() => this.props.submitAction('EducationForm')}>Save</Button>
                </ModalFooter>
            </Modal>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        //TODO remove {job_profile: state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null}
        // initialValues: state.profileEducation.education ? state.profileEducation.education: {},
        initialValues: state.profileEducation.education ? state.profileEducation.education: {job_profile: state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null},
        userId: state.auth.user.id,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
        selectedJobProfile: state.jobProfile.selectedJobProfile,
        isShownEducationEditModal: state.profileEducation.isShownEducationEditModal
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch),
        submitAction: bindActionCreators(submit, dispatch)
    };
};

EducationEditModal = connect(mapStateToProps, mapDispatchToProps)(EducationEditModal);
export default EducationEditModal;
