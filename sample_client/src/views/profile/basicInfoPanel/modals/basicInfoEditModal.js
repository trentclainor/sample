import {Button, Modal, ModalBody, ModalFooter} from "reactstrap";

import React, { Component } from 'react';
import {connect} from "react-redux";
import {SubmissionError, submit} from 'redux-form'

import BasicInfoForm from "../forms/basicInfoForm";

import * as actionCreators from "../../../../actions/profileBasicInfo";
import {bindActionCreators} from "redux";



class BasicInfoEditModal extends Component {
    constructor() {
        super();
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(values){
        let _this = this;
        let action = null;
        let _values = Object.assign({}, values);

        if (_values.photo && typeof _values.photo === 'string'){
            delete _values.photo;
        }
        else if (_values.photo && 'photo' in _values && '0' in _values.photo){
            _values.photo = _values.photo[0]
        }

        if ('id' in values) {
            action = this.props.actions.basicInfoUpdate(this.props.userId, this.props.jobProfileId, _values);
        } else {
            action = this.props.actions.basicInfoCreate(this.props.userId, this.props.jobProfileId, _values);
        }
        return action
            .then(function (response) {
                _this.props.actions.hideBasicInfoEditModal();
            })
            .catch(error => {
                throw new SubmissionError(error.response.data)
            })
    }

    render() {
        return (
            <Modal isOpen={this.props.isShownBasicInfoEditModal} toggle={this.props.actions.hideBasicInfoEditModal}>
                <div className="modal-header bg-brand-gradient">
                    <h5 className="modal-title text-white" id="basicInfoModalTitle">Basic Information</h5>
                    <button type="button" className="close text-white" onClick={this.props.actions.hideBasicInfoEditModal} aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <ModalBody>
                    {this.props.initialValues ?
                        <BasicInfoForm
                            onSubmit={this.handleSubmit}
                            initialValues={this.props.initialValues}
                            enableReinitialize={true}/>
                        :
                        <BasicInfoForm
                            onSubmit={this.handleSubmit}
                            enableReinitialize={true}/>
                    }
                </ModalBody>
                <ModalFooter>
                    <Button color='outline-secondary' onClick={this.props.actions.hideBasicInfoEditModal}>Close</Button>
                    <Button color='brand' onClick={() => this.props.submitAction('BasicInfoForm')}>Save</Button>
                </ModalFooter>
            </Modal>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        initialValues: state.profileBasicInfo.basicInfos.length ? state.profileBasicInfo.basicInfos[0]: null,
        userId: state.auth.user.id,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
        selectedJobProfile: state.jobProfile.selectedJobProfile,
        isShownBasicInfoEditModal: state.profileBasicInfo.isShownBasicInfoEditModal
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch),
        submitAction: bindActionCreators(submit, dispatch)
    };
};

BasicInfoEditModal = connect(mapStateToProps, mapDispatchToProps)(BasicInfoEditModal);
export default BasicInfoEditModal;
