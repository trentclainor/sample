import React, { Component} from 'react';

import { connect } from 'react-redux';
import * as actionCreators from "../../../../actions/profileLanguage";
import {bindActionCreators} from "redux";
import Icon from "../../../../utils/icon";

class LanguageItem extends Component {
    cursorStyles = {
        cursor: 'pointer'
    };

    render() {
        return (
            <div className="d-flex align-items-center bg-light border border-light-dark p-3 mb-2 text-dark">
                <div className="pull-left mr-2">
                    <a href="javascript:void(0)" className="row m-2 cv-mark-default">
                        <Icon name='trash' style={this.cursorStyles} onClick={() => this.props.actions.languageDelete(this.props.userId, this.props.jobProfileId, this.props.language.id)}/>
                    </a>
                    <a href="javascript:void(0)" className="row m-2 cv-mark-default">
                        <Icon name='pencil' style={this.cursorStyles} onClick={() => this.props.actions.showLanguageEditModal(this.props.language)}/>
                    </a>
                </div>
                <span className="logo mr-3">
                    <div className='p-1 border border-light-dark'>
                        <Icon name='globe' size='3x'/>
                    </div>
                </span>
                <dl className="mb-0 mr-auto">
                    <dt>{this.props.language.name}</dt>
                    <dd className="mb-0">{this.props.language.level_display}</dd>
                </dl>
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

LanguageItem = connect(mapStateToProps, mapDispatchToProps)(LanguageItem);

export default LanguageItem;
