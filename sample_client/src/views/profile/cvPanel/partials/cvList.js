import React, { Component} from 'react';
import { connect } from 'react-redux';

import CVItem from './cvItem';

import * as actionCreators from "../../../../actions/jobProfile";
import {bindActionCreators} from "redux";


class CVList extends Component {

    cvList = () => {
        return this.props.jobProfiles.map(jobProfile => {
            let isSelected = false;
            if (this.props.selectedJobProfile !== undefined){
                isSelected = jobProfile.id === this.props.selectedJobProfile.id;
            }

            return (
                <CVItem key={jobProfile.id} jobProfile={jobProfile} isSelected={isSelected} selectJobProfile={this.props.actions.selectJobProfile}/>
            )
        })
    };

    render() {
        return (
            <div>
                {this.cvList()}
            </div>
        )
    }
}

function mapStateToProps(state) {

  return {
      jobProfiles: state.jobProfile.jobProfiles,
      selectedJobProfile: state.jobProfile.selectedJobProfile
  }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(CVList);
