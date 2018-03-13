import React, { Component} from 'react';
import { connect } from 'react-redux';

import EducationItem from './educationItem';


class EducationList extends Component {

    educationList = () => {
        return this.props.educations.map(education => {
            return (
                <EducationItem key={education.id} education={education}/>
            )
        })
    };

    render() {
        return (
            <div>
                {this.educationList()}
            </div>
        )
    }
}

function mapStateToProps(state) {

  return {
      educations: state.profileEducation.educations,
  }
}

export default connect(mapStateToProps)(EducationList);
