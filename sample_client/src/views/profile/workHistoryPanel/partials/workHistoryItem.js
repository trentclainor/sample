import React, { Component} from 'react';

import { connect } from 'react-redux';
import * as actionCreators from "../../../../actions/profileWorkHistory";
import {bindActionCreators} from "redux";
import moment from "moment";
import Icon from "../../../../utils/icon";

class WorkHistoryItem extends Component {
    cursorStyles = {
        cursor: 'pointer'
    };

    render() {
        let end_date = this.props.workHistory.end_date ? this.props.workHistory.end_date: moment().toDate();

        let duration = moment.duration(moment(end_date).diff(this.props.workHistory.start_date)).humanize();
        return (
            <div className="d-flex align-items-center bg-light border border-light-dark p-3 mb-2 text-dark">
                <div className="pull-left mr-2">
                    <a href="javascript:void(0)" className="row m-2 cv-mark-default">
                        <Icon name='trash' style={this.cursorStyles} onClick={() => this.props.actions.workHistoryDelete(this.props.userId, this.props.jobProfileId, this.props.workHistory.id)}/>
                    </a>
                    <a href="javascript:void(0)" className="row m-2 cv-mark-default">
                        <Icon name='pencil' style={this.cursorStyles} onClick={() => this.props.actions.showWorkHistoryEditModal(this.props.workHistory)}/>
                    </a>
                </div>
                <span className="logo mr-3">
                    <div className='p-1 border border-light-dark'>
                        <Icon name='building' size='2x'/>
                        <Icon name='building' size='3x'/>
                        <Icon name='building' size='2x'/>
                    </div>
                </span>
                <dl className="mb-0 mr-auto">
                    <dt>{this.props.workHistory.role}</dt>
                    <dd className="mb-0">{this.props.workHistory.company_name}</dd>
                </dl>
                <ul className="list-unstyled mb-0 text-right">
                    <li>{duration}</li>
                    <li>{this.props.workHistory.start_date} - {this.props.workHistory.end_date ? this.props.workHistory.end_date: "Present"}</li>
                </ul>
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        userId: state.auth.user.id,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

WorkHistoryItem = connect(mapStateToProps, mapDispatchToProps)(WorkHistoryItem);

export default WorkHistoryItem;
