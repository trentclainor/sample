import {Button, Modal, ModalBody, ModalFooter} from "reactstrap";

import React, { Component } from 'react';

import {connect} from "react-redux";
import {SubmissionError, submit} from "redux-form";

import * as actionCreators from "../../../../actions/jobProfile";
import {bindActionCreators} from "redux";

import CVForm from "../forms/cvForm";



class CVEditModal extends Component {
    constructor() {
        super();
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(values){
        let _this = this;
        let action = null;
        let _values = Object.assign({}, values);

        if (_values.cv && typeof _values.cv === 'string'){
            delete _values.cv;
        }
        else if (_values.cv && 'cv' in _values && '0' in _values.cv){
            _values.cv = _values.cv[0]
        }

        if ('id' in _values) {
            action = this.props.actions.jobProfileUpdate(_values);
        } else {
            action = this.props.actions.jobProfileCreate(_values);
        }
        return action
            .then(function (response) {
                _this.props.actions.hideJobProfileEditModal();
            })
            .catch(error => {
                throw new SubmissionError(error.response.data)
            })
    }

    render() {
        return (
            <Modal isOpen={this.props.isShownJobProfileEditModal} toggle={this.props.actions.hideJobProfileEditModal}>
                <div className="modal-header bg-brand-gradient">
                    <h5 className="modal-title text-white" id="basicInfoModalTitle">Upload CV</h5>
                    <button type="button" className="close text-white" onClick={this.props.actions.hideJobProfileEditModal} aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <ModalBody>
                    {this.props.initialValues ?
                        <CVForm
                            onSubmit={this.handleSubmit}
                            initialValues={this.props.initialValues}
                            enableReinitialize={true}/>
                        :
                        <CVForm
                            onSubmit={this.handleSubmit}
                            enableReinitialize={true}/>
                    }
                </ModalBody>
                <ModalFooter>
                    <Button color='outline-secondary' onClick={this.props.actions.hideJobProfileEditModal}>Close</Button>
                    <Button color='brand' onClick={() => this.props.submitAction('CVForm')}>Save</Button>
                </ModalFooter>
            </Modal>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        initialValues: state.jobProfile.jobProfile,
        isShownJobProfileEditModal: state.jobProfile.isShownJobProfileEditModal,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch),
        submitAction: bindActionCreators(submit, dispatch)
    };
};

CVEditModal = connect(mapStateToProps, mapDispatchToProps)(CVEditModal);
export default CVEditModal;
