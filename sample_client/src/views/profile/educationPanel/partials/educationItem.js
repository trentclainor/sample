import React, { Component} from 'react';

import { connect } from 'react-redux';
import * as actionCreators from "../../../../actions/profileEducation";
import {bindActionCreators} from "redux";
import moment from "moment";
import Icon from "../../../../utils/icon";

class EducationItem extends Component {
    cursorStyles = {
        cursor: 'pointer'
    };

    render() {
        let end_date = this.props.education.end_date ? this.props.education.end_date: moment().toDate();

        let duration = moment.duration(moment(end_date).diff(this.props.education.start_date)).humanize();
        return (
            <div className="d-flex align-items-center bg-light border border-light-dark p-3 mb-2 text-dark">
                <div className="pull-left mr-2">
                    <a href="javascript:void(0)" className="row m-2 cv-mark-default">
                        <Icon name='trash' style={this.cursorStyles} onClick={() => this.props.actions.educationDelete(this.props.userId, this.props.jobProfileId, this.props.education.id)}/>
                    </a>
                    <a href="javascript:void(0)" className="row m-2 cv-mark-default">
                        <Icon name='pencil' style={this.cursorStyles} onClick={() => this.props.actions.showEducationEditModal(this.props.education)}/>
                    </a>
                </div>
                <span className="logo mr-3">
                    <div className='p-1 border border-light-dark'>
                        <Icon name='graduation-cap' size='3x'/>
                    </div>
                </span>
                <dl className="mb-0 mr-auto">
                    <dt>{this.props.education.degree}</dt>
                    <dd className="mb-0">{this.props.education.school}</dd>
                </dl>
                <ul className="list-unstyled mb-0 text-right">
                    <li>{duration}</li>
                    {this.props.education.start_date} - {this.props.education.end_date ? this.props.education.end_date: "Present"}
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

EducationItem = connect(mapStateToProps, mapDispatchToProps)(EducationItem);

export default EducationItem;
