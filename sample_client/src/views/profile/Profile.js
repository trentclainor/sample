import React, { Component} from 'react';
import { connect } from 'react-redux';
import {ControlLabel, Form, FormGroup, Panel} from "react-bootstrap";
// layout
import Title from "../../components/partials/Title";
// panels
import CVPanel from "./cvPanel";
import BasicInfoPanel from "./basicInfoPanel";
import WorkHistoryPanel from "./workHistoryPanel";
import EducationPanel from "./educationPanel";
import LanguagePanel from "./languagePanel";
// modals
import CVEditModal from "./cvPanel/modals/cvEditModal";
import BasicInfoEditModal from "./basicInfoPanel/modals/basicInfoEditModal";
import WorkHistoryEditModal from "./workHistoryPanel/modals/workHistoryEditModal";
import EducationEditModal from "./educationPanel/modals/educationEditModal";
import LanguageEditModal from "./languagePanel/modals/languageEditModal";
import SearchPreferencesPanel from "./searchPreferencesPanel";


class Profile extends Component {

  render() {
    return (
      <div className="Profile">
        <Title title='Profile'/>
        <div className="container">
          <div className="row">
            <div className="col-sm-8">
                <CVPanel />
                <CVEditModal />

                <BasicInfoPanel />
                <BasicInfoEditModal />

                <WorkHistoryPanel />
                <WorkHistoryEditModal />

                <EducationPanel />
                <EducationEditModal />

                <LanguagePanel />
                <LanguageEditModal />

            </div>
            <div className="col-sm-4">
                <SearchPreferencesPanel />
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default connect()(Profile);
