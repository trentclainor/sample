import React, { Component } from 'react';
import Title from "../../components/partials/Title";

class NotFoundView extends Component {
  render() {
    return (
      <div className="NotFoundView">
        <Title title='Page not found...'/>
        <div className="container">
          <div className="page-content">
            Page not found...
          </div>
        </div>
      </div>
    );
  }
}

export default NotFoundView;
