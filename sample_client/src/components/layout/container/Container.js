import React, { Component } from 'react';
import routes from '../../../routes';

class Container extends Component {
  render() {
    return (
      <div className="Container">
          {routes}
      </div>
    );
  }
}

export default Container;
