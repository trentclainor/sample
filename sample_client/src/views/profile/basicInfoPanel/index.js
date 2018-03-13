import {Alert, Button, Col, Row} from "reactstrap";

import React, { Component} from 'react';
import { connect } from 'react-redux';

import * as actionCreators from "../../../actions/profileBasicInfo";
import {bindActionCreators} from "redux";
import Icon from "../../../utils/icon";



class BasicInfoPanel extends Component {

    componentDidMount() {
        if (this.props.userId && this.props.jobProfileId){
            this.props.actions.basicInfoList(this.props.userId, this.props.jobProfileId);
        }
    }
    componentWillReceiveProps(nextProps) {
        if (this.props.jobProfileId !== nextProps.jobProfileId && nextProps.jobProfileId){
            nextProps.actions.basicInfoList(nextProps.userId, nextProps.jobProfileId);
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
                Add some new basic info to get started.
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

    jobProfileItems = () => {
        return this.props.basicInfos.map(basicInfo => {
            return (
                <div key={basicInfo.id}>
                    <Row>
                        <Col sm='7'>
                            <dl className="mb-4">
                                <dd>Name</dd>
                                <dt>{basicInfo.name}</dt>
                            </dl>
                            <dl className="mb-4">
                                <dd>Email</dd>
                                <dt>{basicInfo.email}</dt>
                            </dl>
                            <dl className="mb-4">
                                <dd>Phone</dd>
                                <dt>{basicInfo.phone}</dt>
                            </dl>
                            <dl className="mb-4">
                                <dd>Linkedin</dd>
                                <dt>{basicInfo.linkedin}</dt>
                            </dl>
                            <dl className="mb-4">
                                <dd>Address</dd>
                                <dt>{basicInfo.address1} {basicInfo.address2} {basicInfo.address3}</dt>
                            </dl>
                        </Col>
                        <Col sm='5'>
                            {basicInfo.photo ?
                                <div>
                                    <img src={basicInfo.photo} className="img-responsive img-rounded img-thumbnail"/>
                                </div>
                                :
                                ''
                            }
                        </Col>
                    </Row>
                </div>
        )
        })
        };

        jobProfileList = () => {
            return (
            <div>
            {this.jobProfileItems()}
            </div>
            )
        };

        basicInfoPanel = () => {
            return (
            <div className="bg-white p-3 mb-3">
            <h4 className="border-bottom border-brand">
            Basic Information
            <Button className='pull-right' size='sm' color='primary' onClick={this.props.actions.showBasicInfoEditModal}>
            <Icon name='pencil'/>
            </Button>
            </h4>
            {this.props.loading && this.loadingMessage()}
            {this.props.basicInfos.length === 0 && !this.props.loading && !this.props.errors.global && this.emptyMessage()}
            {this.props.errors.global && this.timeoutMessage()}
            {this.props.basicInfos.length > 0 && this.jobProfileList()}

            </div>
            )
        };

        render() {
            return (
            <div>
            {this.props.jobProfileId && this.basicInfoPanel()}
            </div>
            )
        }
        }

        function mapStateToProps(state) {

            return {
            userId: state.auth.user.id,
            basicInfos: state.profileBasicInfo.basicInfos,
            jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
            loading: state.profileBasicInfo.loading,
            errors: state.profileBasicInfo.errors,
        }
        }

        const mapDispatchToProps = (dispatch) => {
            return {
            dispatch,
            actions: bindActionCreators(actionCreators, dispatch),
        };
        };

        BasicInfoPanel = connect(mapStateToProps, mapDispatchToProps)(BasicInfoPanel);
        export default BasicInfoPanel;
