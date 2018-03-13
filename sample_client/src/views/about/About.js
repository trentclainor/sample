import React, { Component } from 'react';
import Title from "../../components/partials/Title";

class AboutView extends Component {
  render() {
    return (
      <div className="AboutView">
        <Title title='About'/>
        <div className="container">
          <div className="page-content">
            AboutView content
          </div>
        </div>
      </div>
    );
  }
}

export default AboutView;
