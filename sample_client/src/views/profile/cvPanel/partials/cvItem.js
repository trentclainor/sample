import React, { Component} from 'react';
import { connect } from 'react-redux';
import * as actionCreators from "../../../../actions/jobProfile";
import {bindActionCreators} from "redux";
import moment from "moment";
import Icon from "../../../../utils/icon";

class CVItem extends Component {
    cursorStyles = {
        textAlign: 'center',
        cursor: 'pointer'
    };


    render() {
        let modified = moment(this.props.jobProfile.modified).format('DD MMM YYYY');
        let borderColor = this.props.isSelected ? 'border-secondary': 'border-light-dark';
        return (
            <div className={'d-flex align-items-center bg-light border p-3 mb-2 text-dark ' + borderColor}>
                <div className="pull-left mr-2">
                    <a href="javascript:void(0)" className="row m-2 cv-mark-default">
                        <Icon name='trash' style={this.cursorStyles} onClick={() => this.props.actions.jobProfileDelete(this.props.jobProfile.id)}/>
                    </a>
                    <a href="javascript:void(0)" className="row m-2 cv-mark-default">
                        <Icon name='pencil' style={this.cursorStyles} onClick={() => this.props.actions.showJobProfileEditModal(this.props.jobProfile)}/>
                    </a>
                </div>
                <span className="icon mr-3">
                    <Icon name='file-text-o'/>
                </span>
                <dl className="mb-0 mr-auto" onClick={() => this.props.actions.selectJobProfile(this.props.jobProfile)}>
                    <dt>
                        <a href="javascript:void(0)">{this.props.jobProfile.name}</a>
                    </dt>
                    <dd className="mb-0">Updated On: {modified}</dd>
                </dl>
                {this.props.jobProfile.is_default===true ?
                    <a href="javascript:void(0)" className="cv-mark-default active d-block text-center">
                        <Icon name='check-circle' size='2x'/>
                        <br/>
                        <small>Default</small>
                    </a>
                    :
                    <a href="javascript:void(0)" className="cv-mark-default d-block text-center" onClick={() => this.props.actions.jobProfileMarkDefault(this.props.jobProfile.id)}>
                        <Icon name='check-circle' size='2x'/>
                        <br/>
                        <small>Mark Default</small>
                    </a>
                }
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        userId: state.auth.user.id,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

CVItem = connect(mapStateToProps, mapDispatchToProps)(CVItem);

export default CVItem;
