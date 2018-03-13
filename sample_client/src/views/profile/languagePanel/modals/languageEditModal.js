import {Button, Modal, ModalBody, ModalFooter} from "reactstrap";

import React, { Component } from 'react';

import {connect} from "react-redux";

import LanguageForm from "../forms/languageForm";
import {SubmissionError, submit} from 'redux-form'

import * as actionCreators from "../../../../actions/profileLanguage";
import {bindActionCreators} from "redux";



class LanguageEditModal extends Component {
    constructor() {
        super();
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(values){
        let _this = this;
        let action = null;
        if ('id' in values) {
            action = this.props.actions.languageUpdate(this.props.userId, this.props.jobProfileId, values);
        } else {
            action = this.props.actions.languageCreate(this.props.userId, this.props.jobProfileId, values);
        }
        return action
            .then(function (response) {
                _this.props.actions.hideLanguageEditModal();
            })
            .catch(error => {
                throw new SubmissionError(error.response.data)
            })
    }

    render() {
        return (
            <Modal isOpen={this.props.isShownLanguageEditModal} toggle={this.props.actions.hideLanguageEditModal}>
                <div className="modal-header bg-brand-gradient">
                    <h5 className="modal-title text-white" id="basicInfoModalTitle">Language</h5>
                    <button type="button" className="close text-white" onClick={this.props.actions.hideLanguageEditModal} aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <ModalBody>
                    {this.props.initialValues ?
                        <LanguageForm
                            onSubmit={this.handleSubmit}
                            initialValues={this.props.initialValues}
                            enableReinitialize={true}/>
                        :
                        <LanguageForm
                            onSubmit={this.handleSubmit}
                            enableReinitialize={true}/>
                    }
                </ModalBody>
                <ModalFooter>
                    <Button color='outline-secondary' onClick={this.props.actions.hideLanguageEditModal}>Close</Button>
                    <Button color='brand' onClick={() => this.props.submitAction('LanguageForm')}>Save</Button>
                </ModalFooter>
            </Modal>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        initialValues: state.profileLanguage.language ? state.profileLanguage.language: null,
        userId: state.auth.user.id,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
        selectedJobProfile: state.jobProfile.selectedJobProfile,
        isShownLanguageEditModal: state.profileLanguage.isShownLanguageEditModal
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch),
        submitAction: bindActionCreators(submit, dispatch)
    };
};

LanguageEditModal = connect(mapStateToProps, mapDispatchToProps)(LanguageEditModal);
export default LanguageEditModal;
